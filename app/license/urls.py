from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from license.api import LicenseDetailAPI

router = routers.DefaultRouter()

router.register(r"web/license", LicenseDetailAPI, basename="licenses")

urlpatterns = []

urlpatterns += router.urls + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
