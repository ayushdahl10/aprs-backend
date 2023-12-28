from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers

from website.apis import DepartmentAPI
from website.views import generate_pdf

router = routers.DefaultRouter()

router.register(r"web/department", DepartmentAPI, basename="departments")

urlpatterns = [
    path("generate-pdf/", generate_pdf, name="generate_pdf"),
    # other URL patterns...
]

urlpatterns += router.urls + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
