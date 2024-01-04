from helpers.super_viewset import SuperViewset
from property.models import Property, Tenant
from property.serializers import (
    PropertySerializerDetail,
    PropertySerializerCreate,
    PropertySerializerList,
    TenantSerializerList,
    TenantSerializerDetail,
    TenantSerializerCreate,
)


class PropertyAPI(SuperViewset):
    queryset = Property.objects.filter(is_deleted=False, is_active=True)
    list_serializer = PropertySerializerList
    detail_serializer = PropertySerializerDetail
    create_serializer = PropertySerializerCreate


class TenantAPI(SuperViewset):
    queryset = Tenant.objects.filter(is_active=True, is_deleted=False)
    list_serializer = TenantSerializerList
    detail_serializer = TenantSerializerDetail
    create_serializer = TenantSerializerCreate
