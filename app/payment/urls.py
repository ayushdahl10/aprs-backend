from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers

from payment.api import PayAPI

urlpatterns = []

router = routers.DefaultRouter()

router.register(r"web/payment", PayAPI, basename="payment-method")


urlpatterns += router.urls + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
