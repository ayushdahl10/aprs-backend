import django_filters

from autho.models import Attendance


class CalenderFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Attendance
        fields = [
            "date",
        ]
