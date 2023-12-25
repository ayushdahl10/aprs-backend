from django.urls import path
from autho.apis import RegisterAPI, LoginAPI, UserDetailAPI, ValidateTokenAPI, StaffAPI
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    path("web/register", RegisterAPI.as_view(), name="user_register"),
    path("web/login", LoginAPI.as_view(), name="user_login"),
    path("web/user/<str:pk>", UserDetailAPI.as_view(), name="user_detail"),
    path("web/token", ValidateTokenAPI.as_view(), name="validatetoken"),
]

router.register("web/staff", StaffAPI, basename="staffs")

urlpatterns += router.urls

# # Only use static during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
