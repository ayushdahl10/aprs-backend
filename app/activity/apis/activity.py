from activity.filters import CalenderFilter
from activity.serializer import CalenderListSerializer, CalenderDetailSerializer
from autho.models import Attendance, Staff
from helpers.exceptions import NotFoundException
from helpers.readony_viewset import ReadOnlyViewSet


class AttendanceAPI(ReadOnlyViewSet):
    queryset = Attendance.objects.filter(is_deleted=False, is_active=True)
    list_serializer = CalenderListSerializer
    detail_serializer = CalenderDetailSerializer
    filterset_class = CalenderFilter
    required_param = ["date_after", "date_before"]

    def list(self, request, *args, **kwargs):

        try:
            staff = Staff.objects.get(user__user=self.request.user)
        except Staff.DoesNotExists:
            raise NotFoundException("You are not a valid staff")
        queryset = self.get_queryset().filter(staff=staff)
        return super().list(request=request, queryset=queryset)
