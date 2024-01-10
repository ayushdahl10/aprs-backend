import django_filters

from autho.models import Attendance, AttendanceRequest


class CalenderFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Attendance
        fields = [
            "date",
        ]


class AttendanceRequestFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = AttendanceRequest
        fields = [
            "status",
        ]
