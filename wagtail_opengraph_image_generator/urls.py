from django.urls import path

from .apps import WagtailOGImageGeneratorConfig
from .views import show_preview

app_name = WagtailOGImageGeneratorConfig.name
urlpatterns = [path('preview/<int:page_id>/', show_preview, name='show_preview')]
