from rest_framework import serializers

from helpers.base_serializer import BaseModelSerializer
from website.models import Department, Company


class CompanyListSerializer(BaseModelSerializer):
    class Meta:
        model = Company
        fields = [
            "iid",
            "company_name",
            "company_logo",
            "country",
            "address",
            "is_active",
        ]


class CompanyCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Company
        fields = [
            "iid",
            "company_name",
            "company_logo",
            "country",
            "address",
            "contact_info",
            "pan_number",
            "company_vat",
            "terms_and_conditions",
        ]


class CompanyDetailSerializer(BaseModelSerializer):
    class Meta:
        model = Company
        fields = [
            "iid",
            "company_name",
            "company_logo",
            "country",
            "address",
            "contact_info",
            "pan_number",
            "company_vat",
            "terms_and_conditions",
            "is_active",
        ]


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

    def validate_name(self, value):
        if self.Meta.model.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                f"fDepartment with name {value} already exists"
            )
        return value

    def create(self, validated_data):
        validated_data["created_by"] = self.context.get("request").user
        validated_data["is_active"] = True
        return super().create(validated_data)
