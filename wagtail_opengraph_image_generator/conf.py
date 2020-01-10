from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


PREFIX = 'WAGTAIL_OG_IMAGE_GENERATOR_'

DEFAULT_SETTINGS = {
    'IMAGE_WIDTH': 1200,
    'IMAGE_HEIGHT': 630,
    'IMAGE_PADDING': 32,
    'COLLECTION_NAME': 'OpenGraph',
    'TAB_NAME': 'OpenGraph Image',
    'PAGE_MODEL': 'wagtailcore.Page',
    'CREATE_AUTOMATICALLY': True,
    'FIELD_SUBTITLE': '',
    'FIELD_BACKGROUND_IMAGE': '',
    'FIELD_LOGO': '',
}


def setting(name):
    return getattr(settings, '{}{}'.format(PREFIX, name), DEFAULT_SETTINGS[name])


def get_page_model():
    page = setting('PAGE_MODEL')

    try:
        return apps.get_model(page, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "WAGTAIL_OG_IMAGE_GENERATOR_PAGE_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "WAGTAIL_OG_IMAGE_GENERATOR_PAGE_MODEL refers to model '{}' that has not been installed".format(
                page
            )
        )
