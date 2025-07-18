from helpers.super_viewset import SuperViewset
from website.models import Department, Company
from website.serializer import (
    DepartmentListSerializer,
    DepartmentDetailSerializer,
    DepartmentCreateSerializer,
    CompanyCreateSerializer,
    CompanyListSerializer,
    CompanyDetailSerializer,
)


class CompanyAPI(SuperViewset):
    queryset = Company.objects.filter(is_deleted=False, is_active=True)
    create_serializer = CompanyCreateSerializer
    list_serializer = CompanyListSerializer
    detail_serializer = CompanyDetailSerializer


class DepartmentAPI(SuperViewset):
    queryset = Department.objects.filter(is_deleted=False, is_active=True)
    list_serializer = DepartmentListSerializer
    detail_serializer = DepartmentDetailSerializer
    create_serializer = DepartmentCreateSerializer
