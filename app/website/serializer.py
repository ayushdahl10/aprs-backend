from rest_framework import serializers

from helpers.base_serializer import BaseModelSerializer
from website.models import Department


class DepartmentListSerializer(BaseModelSerializer):
    class Meta:
        model = Department
        fields = [
            "iid",
            "name",
        ]


class DepartmentDetailSerializer(BaseModelSerializer):
    class Meta:
        model = Department
        fields = [
            "iid",
            "name",
            "description",
            "contact_info",
        ]


class DepartmentCreateSerializer(BaseModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    contact_info = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Department
        fields = [
            "iid",
            "name",
            "description",
            "contact_info",
            "is_active",
        ]

    def create(self, validated_data):
        validated_data["created_by"] = self.context.get("request").user
        validated_data["is_active"] = True
        return super().create(validated_data)
