from django import template

register = template.Library()

from wagtail_opengraph_image_generator.models import OpenGraphImage
from wagtail_opengraph_image_generator.conf import setting as get_setting


@register.simple_tag()
def get_existing_og_image(page):
    try:
        obj = OpenGraphImage.objects.get(page=page)
        return obj.image
    except OpenGraphImage.DoesNotExist:
        return None


@register.simple_tag()
def get_og_image_generator_setting(setting):
    return get_setting(setting)
