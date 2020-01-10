import os
import html
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from cairosvg import svg2png

from django.utils.html import strip_tags
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.templatetags.static import static

from wagtail.core.models import Collection
from wagtail.images.models import Image as WagtailImage
from wagtail.documents.models import Document

from .conf import setting
from .models import OpenGraphImageGeneratorSettings


def get_font_height(font, text):
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
    total_line_height = offset_y + (ascent - offset_y) + descent
    return total_line_height


def create_og_image(request, page, browser_output=False, extra_data={}):
    OG_WIDTH = setting('IMAGE_WIDTH')
    OG_HEIGHT = setting('IMAGE_HEIGHT')
    OG_PADDING = setting('IMAGE_PADDING')

    TEXT_START_X = OG_PADDING
    TEXT_START_Y = OG_HEIGHT - OG_PADDING
    COLOR_WHITE = (255, 255, 255, 255)
    COLOR_BLACK = (0, 0, 0, 255)

    folder = os.path.dirname(os.path.dirname(__file__))

    og_generator_settings = OpenGraphImageGeneratorSettings.for_site(request.site)

    if og_generator_settings.default_background_image:
        og_default_bg_image = Image.open(
            og_generator_settings.default_background_image.file.path
        )
    else:
        og_default_bg_image = None

    try:
        font_bold = ImageFont.truetype(
            '{}/wagtail_opengraph_image_generator/static/wagtail_opengraph_image_generator/fonts/opensans-bold.ttf'.format(
                folder
            ),
            42,
        )
        font_regular = ImageFont.truetype(
            '{}/wagtail_opengraph_image_generator/static/wagtail_opengraph_image_generator/fonts/opensans-regular.ttf'.format(
                folder
            ),
            42,
        )
    except OSError:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()

    overlay_type = extra_data.get('variant', 'light')
    if overlay_type == 'dark':
        if og_generator_settings.company_logo_alternative:
            company_logo = Image.open(
                og_generator_settings.company_logo_alternative.file.path
            )
        else:
            company_logo = None
        fade = Image.open(
            '{}/wagtail_opengraph_image_generator/static/wagtail_opengraph_image_generator/fade_black.png'.format(
                folder
            )
        )
        color = COLOR_WHITE
    else:
        if og_generator_settings.company_logo:
            company_logo = Image.open(og_generator_settings.company_logo.file.path)
        else:
            company_logo = None
        fade = Image.open(
            '{}/wagtail_opengraph_image_generator/static/wagtail_opengraph_image_generator/fade_white.png'.format(
                folder
            )
        )
        color = COLOR_BLACK

    og_canvas = Image.new('RGB', (OG_WIDTH, OG_HEIGHT))

    # Add background image & company logo to the canvas
    fade = fade.resize((OG_WIDTH, OG_HEIGHT))
    preview_header_image = extra_data.get('background_image', None)
    og_bg_image = None
    if preview_header_image:
        og_bg_image = Image.open(WagtailImage.objects.get(pk=preview_header_image).file)
    else:
        page_background_image = getattr(page, setting('FIELD_BACKGROUND_IMAGE'), None)
        if page_background_image and browser_output is False:
            og_bg_image = Image.open(page_background_image.file.path)
        else:
            og_bg_image = og_default_bg_image

    if og_bg_image:
        og_bg_image = ImageOps.fit(og_bg_image, (OG_WIDTH, OG_HEIGHT), Image.ANTIALIAS)
        og_canvas.paste(og_bg_image, (0, 0))
        og_canvas.paste(fade, (0, 0), fade)
    else:
        if color == COLOR_BLACK:
            og_canvas.paste(COLOR_WHITE, [0, 0, OG_WIDTH, OG_HEIGHT])
        elif color == COLOR_WHITE:
            og_canvas.paste(COLOR_BLACK, [0, 0, OG_WIDTH, OG_HEIGHT])
    if company_logo:
        og_canvas.paste(company_logo, (OG_PADDING, OG_PADDING), company_logo)

    drawable = ImageDraw.Draw(og_canvas)

    # Prepare subtitle lines to see where we start drawing stuff
    preview_text = extra_data.get('subtitle', None)
    if preview_text:
        og_text_lines = preview_text.split('</span></span></div></div>')
    else:
        subtitle_field = getattr(page, setting('FIELD_SUBTITLE'), None)
        if subtitle_field and browser_output is False:
            og_text_lines = subtitle_field.split('</p><p>')
        else:
            og_text_lines = None

    if og_text_lines:
        og_text_lines = list(filter(None, map(lambda x: strip_tags(x), og_text_lines)))
        num_lines = len(og_text_lines)
    else:
        num_lines = 0

    # Calculate font sizes to correctly ascertain starting position
    if num_lines > 0:
        curY = TEXT_START_Y - (
            get_font_height(font_regular, og_text_lines[0]) * (num_lines + 1)
        )
    else:
        curY = TEXT_START_Y - get_font_height(
            font_bold, extra_data.get('title', page.title)
        )

    # Convert optional page SVG icon to PNG and add it to the canvas
    logo_file = None
    preview_logo = extra_data.get('logo', None)
    if preview_logo:
        logo_file = Document.objects.get(pk=preview_logo).file
    else:
        page_logo = getattr(page, setting('FIELD_LOGO'), None)
        if page_logo and browser_output is False:
            logo_file = page_logo.file
    if logo_file:
        png_icon_str = svg2png(file_obj=logo_file)
        png_icon = Image.open(BytesIO(png_icon_str))
        curY -= png_icon.height
        og_canvas.paste(png_icon, (OG_PADDING, curY), png_icon)
        curY += png_icon.height + 8

    # Draw the page title
    drawable.text(
        (TEXT_START_X, curY),
        extra_data.get('title', page.title),
        font=font_bold,
        fill=color,
    )
    curY += get_font_height(font_bold, extra_data.get('title', page.title)) + 4

    # Draw the subtitle lines
    if og_text_lines:
        for line in og_text_lines:
            line = html.unescape(line)  # unescape to allow entities like '&'
            drawable.text((TEXT_START_X, curY), line, font=font_regular, fill=color)
            curY += get_font_height(font_regular, line)

    # Create image
    og_file_name = 'og_{}.png'.format(page.slug)
    buf = BytesIO()
    og_canvas.save(buf, format='PNG')
    buf.seek(0)

    if browser_output:
        return buf
    else:
        # Get correct Collection or create if it doesn't exist
        try:
            collection = Collection.objects.get(name=setting('COLLECTION_NAME'))
        except Collection.DoesNotExist:
            collection = Collection(name=setting('COLLECTION_NAME'))
            root_collection = Collection.get_first_root_node()
            root_collection.add_child(instance=collection)

        # Clear other/older versions of the page's generated OG images
        WagtailImage.objects.filter(title=og_file_name, collection=collection).delete()

        # Convert Django image to Wagtail image
        django_image = InMemoryUploadedFile(
            buf, 'open_graph_image', og_file_name, 'image/png', buf.tell(), None
        )
        wagtail_image = WagtailImage(
            title=og_file_name, file=django_image, collection=collection
        )
        wagtail_image.save()

        # Return new OG image
        return wagtail_image
