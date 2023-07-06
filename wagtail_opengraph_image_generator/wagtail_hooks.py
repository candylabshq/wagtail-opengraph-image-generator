from django.conf.urls import include
from django.urls import path
from django.utils.html import format_html
from django.templatetags.static import static

from wagtail import hooks
from wagtail.admin.panels import ObjectList, extract_panel_definitions_from_model_class, HelpPanel
from wagtail.utils.decorators import cached_classmethod

from .conf import setting, get_page_model
from .generator import create_og_image
from .models import OpenGraphImage


class OpenGraphTemplateTab(ObjectList):
    template = 'wagtail_opengraph_image_generator/opengraph_tab.html'


@cached_classmethod
def get_edit_handler(cls):
    if hasattr(cls, "edit_handler"):
        edit_handler = cls.edit_handler
    else:
        panels = extract_panel_definitions_from_model_class(cls)
        edit_handler = ObjectList(panels)

    tab = OpenGraphTemplateTab(
        [HelpPanel(template="wagtail_opengraph_image_generator/opengraph_tab.html")], heading=setting('TAB_NAME')
    )
    edit_handler.children.append(tab)

    return edit_handler.bind_to_model(cls)


get_page_model().get_edit_handler = get_edit_handler


@hooks.register('after_edit_page')
@hooks.register('after_create_page')
def save_og_image(request, page):
    if not isinstance(page, get_page_model()):
        return

    if setting('CREATE_AUTOMATICALLY') or request.POST.get('og_save', ''):
        OpenGraphImage.objects.filter(page=page).delete()

        og_image = OpenGraphImage()
        og_image.page = page
        og_image.image = create_og_image(
            request,
            page,
            False,
            {'variant': request.POST.get('og_dark_variant', 'light')},
        )
        og_image.save()


@hooks.register('insert_editor_js')
def add_og_js():
    str_js = format_html(
        '''
        <script>
            const OG_FIELD_TITLE = '{}'
            const OG_FIELD_SUBTITLE = '{}'
            const OG_FIELD_BACKGROUND_IMAGE = '{}'
            const OG_FIELD_LOGO = '{}'
        </script>
    '''.format(
            setting('FIELD_TITLE'),
            setting('FIELD_SUBTITLE'),
            setting('FIELD_BACKGROUND_IMAGE'),
            setting('FIELD_LOGO'),
        )
    )
    return str_js + format_html(
        '<script src="{}"></script>'.format(static('wagtail_opengraph_image_generator/scripts.js'))
    )


@hooks.register('register_admin_urls')
def register_admin_urls():
    from . import urls

    return [
        path(
            'wagtail_opengraph_image_generator/',
            include((urls, 'wagtail_opengraph_image_generator')),
        )
    ]
