from helpers.super_viewset import SuperViewset
from website.models import Department
from website.serializer import (
    DepartmentListSerializer,
    DepartmentDetailSerializer,
    DepartmentCreateSerializer,
)


class DepartmentAPI(SuperViewset):
    queryset = Department.objects.filter(is_active=True)
    list_serializer = DepartmentListSerializer
    detail_serializer = DepartmentDetailSerializer
    create_update_serializer = DepartmentCreateSerializer
