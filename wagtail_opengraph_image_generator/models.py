from django.db import models

from wagtail.images import get_image_model_string
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.panels import FieldPanel

from .conf import get_page_model


class OpenGraphImage(models.Model):
    page = models.ForeignKey(
        get_page_model(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+',
    )
    image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+',
    )

    class Meta:
        unique_together = ['page', 'image']


@register_setting
class OpenGraphImageGeneratorSettings(BaseSetting):
    default_background_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+',
        help_text='Will be used as a fallback background image for your OpenGraph images if no model specific image field has been defined.',
    )
    company_logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+',
        help_text='Will be added to the top left of every OpenGraph image.',
    )
    company_logo_alternative = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+',
        help_text='Alternative version of your logo for the dark OpenGraph image variant. You may want to supply a differently colored logo.',
    )

    panels = [
        FieldPanel('default_background_image'),
        FieldPanel('company_logo'),
        FieldPanel('company_logo_alternative'),
    ]
