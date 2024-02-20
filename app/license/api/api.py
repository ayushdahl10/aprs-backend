from helpers.super_viewset import SuperViewset
from license.models import License
from license.serializers.serializer import LicenseDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action


class LicenseDetailAPI(SuperViewset):
    queryset = License.objects.filter(is_active=True, is_deleted=False)
    serializer_class = LicenseDetailSerializer

    @action(methods=["get"], detail=False, url_path="my-license")
    def get_my_license(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            client__userdetail__user=self.request.user
        )
        if queryset.exists():
            serializer = LicenseDetailSerializer(queryset.first())
            return self.on_api_success_response(serializer.data, status=200)
        return self.on_api_error_response(
            "License detail not found.Please contact your service provider", status=400
        )

    @action(methods=["get"], detail=False, url_path="validate-user")
    def validate_username(self, request, *args, **kwargs):
        username = self.request.GET.get("username", None)
        if username is None:
            return self.on_api_error_response("Username is required in param")
        queryset = self.get_queryset().filter(
            client__userdetail__user__username=username
        )
        if queryset.exists():
            return self.on_api_success_response({"username": username}, status=200)
        return self.on_api_error_response("Invalid Username", status=400)
