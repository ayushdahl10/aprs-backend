from helpers.base_serializer import BaseModelSerializer
from website.models import Department


class DepartmentListSerializer(BaseModelSerializer):
    class Meta:
        model = Department
        fields = [
            "iid",
            "name",
        ]
