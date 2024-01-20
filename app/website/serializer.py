from rest_framework import serializers

from helpers.base_serializer import BaseModelSerializer
from website.models import Company


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
