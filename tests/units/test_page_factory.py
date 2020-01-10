import pytest

from tests.factories.page import PageFactory


@pytest.mark.django_db
class TestPageFactory:
    def test_page_creation(self, client):
        page = PageFactory(depth=1)
        assert page.title == 'My basic page'
