from django.conf.urls import include
from django.urls import path
from django.utils.html import format_html
from django.templatetags.static import static

from wagtail.core import hooks
from wagtail.admin.edit_handlers import FieldPanel, ObjectList

from .conf import setting, get_page_model
from .generator import create_og_image
from .models import OpenGraphImage


class OpenGraphTemplateTab(ObjectList):
    template = 'wagtail_opengraph_image_generator/opengraph_tab.html'


@hooks.register('before_edit_page')
@hooks.register('before_create_page')
def add_og_tab(request, page):
    if not isinstance(page, get_page_model()):
        return

    tab = OpenGraphTemplateTab([], heading=setting('TAB_NAME'))
    children = page.get_edit_handler().children
    exists = False
    for child in children:
        if child.heading == tab.heading:
            exists = True
    if not exists:
        children.append(tab)


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
            const OG_FIELD_SUBTITLE = '{}'
            const OG_FIELD_BACKGROUND_IMAGE = '{}'
            const OG_FIELD_LOGO = '{}'
        </script>
    '''.format(
            setting('FIELD_SUBTITLE'),
            setting('FIELD_BACKGROUND_IMAGE'),
            setting('FIELD_LOGO'),
        )
    )
    return str_js + format_html(
        '<script src="{}"></script>'.format(
            static('wagtail_opengraph_image_generator/scripts.js')
        )
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
