from django.urls import path
from rest_framework import routers

from autho.apis import RegisterAPI, LoginAPI, UserDetailAPI, ValidateTokenAPI, StaffAPI

router = routers.DefaultRouter()

urlpatterns = [
    path("web/register/", RegisterAPI.as_view(), name="user_register"),
    path("web/login/", LoginAPI.as_view(), name="user_login"),
    path("web/user/<str:pk>", UserDetailAPI.as_view(), name="user_detail"),
    path("web/me/", ValidateTokenAPI.as_view(), name="validatetoken"),
]

router.register("web/staff", StaffAPI, basename="staffs")

urlpatterns += router.urls

# # Only use static during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
