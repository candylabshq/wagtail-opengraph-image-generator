import factory

from wagtail.core.models import Page


class PageFactory(factory.DjangoModelFactory):
    title = 'My basic page'
    depth = 2
    path = 'empty'

    class Meta:
        model = Page
