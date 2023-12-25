from rest_framework import routers
from property.apis import PropertyAPI, TenantAPI
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

router.register(r"web/property", PropertyAPI, basename="properties")
router.register(r"web/tenant", TenantAPI, basename="tenants")
urlpatterns = router.urls + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
