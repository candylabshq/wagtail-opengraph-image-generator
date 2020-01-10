import pytest
import base64

from PIL import Image
from io import BytesIO

from django.urls import reverse

from tests.factories.page import PageFactory
from tests.factories.user import UserFactory
from tests.utils import isBase64


@pytest.mark.django_db
class TestViewPreviewGeneration:
    def setup(self):
        self.page = PageFactory()
        self.user = UserFactory(is_superuser=True)

    def test_view_preview_valid(self, client):
        client.force_login(user=self.user)
        response = client.post(
            reverse(
                'wagtail_opengraph_image_generator:show_preview',
                kwargs={'page_id': self.page.id},
            )
        )
        generated_image = response.content
        assert response['Content-Type'] == 'text/plain'
        assert isBase64(generated_image)

    def test_view_preview_image(self, client):
        client.force_login(user=self.user)
        response = client.post(
            reverse(
                'wagtail_opengraph_image_generator:show_preview',
                kwargs={'page_id': self.page.id},
            )
        )
        generated_image = response.content
        image = Image.open(BytesIO(base64.b64decode(generated_image)))
        assert image.width == 1200
        assert image.height == 630
        assert image.format == 'PNG'


@pytest.mark.django_db
class TestViewAccess:
    def setup(self):
        self.user = UserFactory()
        self.admin = UserFactory(is_superuser=True)
        self.page = PageFactory()

    def test_view_access_not_logged_in(self, client):
        response = client.post(
            reverse(
                'wagtail_opengraph_image_generator:show_preview',
                kwargs={'page_id': self.page.id},
            )
        )
        assert response.status_code == 302

    def test_view_access_logged_in_no_admin(self, client):
        client.force_login(user=self.user)
        response = client.post(
            reverse(
                'wagtail_opengraph_image_generator:show_preview',
                kwargs={'page_id': self.page.id},
            )
        )
        assert response.status_code == 302

    def test_view_access_logged_in_admin(self, client):
        client.force_login(user=self.admin)
        response = client.post(
            reverse(
                'wagtail_opengraph_image_generator:show_preview',
                kwargs={'page_id': self.page.id},
            )
        )
        assert response.status_code == 200
