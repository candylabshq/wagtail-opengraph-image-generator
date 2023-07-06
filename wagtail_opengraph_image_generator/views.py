import base64

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from wagtail.models import Page

from .conf import get_page_model
from .generator import create_og_image


@csrf_exempt
def show_preview(request, page_id):
    if page_id > 0:
        page = get_page_model().objects.get(pk=page_id).specific
    else:
        page = None
    buf = create_og_image(request, page, True, request.POST)
    return HttpResponse(base64.b64encode(buf.getvalue()), content_type='text/plain')
