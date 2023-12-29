from activity.filters import CalenderFilter
from activity.serializer import CalenderListSerializer
from autho.models import Attendance, Staff
from helpers.exceptions import NotFoundException
from helpers.super_viewset import ReadOnlyViewSet


class AttendanceAPI(ReadOnlyViewSet):
    queryset = Attendance.objects.filter(is_deleted=False)
    serializer_class = CalenderListSerializer
    filterset_class = CalenderFilter

    def list(self, request, *args, **kwargs):
        try:
            staff = Staff.objects.get(user__user=self.request.user)
        except Staff.DoesNotExists:
            raise NotFoundException("You are not a valid staff")
        queryset = self.get_queryset().filter(staff=staff)
        print(queryset)
        return super().list(request=request, queryset=queryset)
