from property.models import Property, Tenant, LeaseInformation
from helpers.super_viewset import SuperViewset

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from property.serializers import (
    PropertySerializerDetail,
    PropertySerializerCreate,
    PropertySerializerList,
    TenantSerializerList,
    TenantSerializerDetail,
    TenantSerializerCreate,
)
from helpers.pagination import CustomPagination


class PropertyAPI(SuperViewset):
    queryset = Property.objects.filter(is_deleted=False, is_active=True)
    list_serializer = PropertySerializerList
    detail_serializer = PropertySerializerDetail
    create_update_serializer = PropertySerializerCreate


class TenantAPI(SuperViewset):
    queryset = Tenant.objects.filter(is_active=True, is_deleted=False)
    list_serializer = TenantSerializerList
    detail_serializer = TenantSerializerDetail
    create_update_serializer = TenantSerializerCreate
