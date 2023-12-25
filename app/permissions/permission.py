from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authtoken.models import Token
from rest_framework import reverse
from permissions.managepermission.helpers import check_user_permissions
from django.urls import resolve


class WebPermission(BasePermission):
    def has_permission(self, request, view):
        url_name = resolve(request.path).url_name
        has_permission = check_user_permissions(request.user, url_name, request.method)
        return has_permission
