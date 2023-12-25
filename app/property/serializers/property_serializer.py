from helpers.base_serializer import BaseModelSerializer
from property.models import Property, Tenant
from rest_framework import serializers


class PropertySerializerDetail(BaseModelSerializer):
    class Meta:
        model = Property
        fields = [
            "iid",
            "name",
            "gallery",
            "owner",
            "location",
            "description",
            "is_active",
        ]


class PropertySerializerList(BaseModelSerializer):
    class Meta:
        model = Property
        fields = [
            "iid",
            "name",
            "owner",
            "location",
            "description",
            "is_active",
        ]


class PropertySerializerCreate(BaseModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Property
        fields = [
            "iid",
            "name",
            "gallery",
            "description",
            "location",
            "owner",
            "is_active",
        ]


class TenantSerializerList(BaseModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            "iid",
            "title",
            "property",
            "is_active",
        ]


class TenantSerializerDetail(BaseModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            "iid",
            "title",
            "property",
            "start_date",
            "end_date",
            "is_active",
        ]


class TenantSerializerCreate(BaseModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Tenant
        fields = [
            "iid",
            "title",
            "property",
            "start_date",
            "end_date",
            "is_active",
        ]

    def create(self, validated_data):
        validated_data["created_by"] = self.context.get("request").user
        return super().create(validated_data)
