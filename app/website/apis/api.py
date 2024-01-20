from helpers.super_viewset import SuperViewset
from website.models import Company
from website.serializer import (
    CompanyCreateSerializer,
    CompanyListSerializer,
    CompanyDetailSerializer,
)


class CompanyAPI(SuperViewset):
    queryset = Company.objects.filter(is_deleted=False, is_active=True)
    create_serializer = CompanyCreateSerializer
    list_serializer = CompanyListSerializer
    detail_serializer = CompanyDetailSerializer
