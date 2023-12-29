import django_filters

from autho.models import Attendance


class CalenderFilter(django_filters.FilterSet):
    check_in = django_filters.DateFilter()
    check_out = django_filters.DateFilter()

    class Meta:
        model = Attendance
        fields = [
            "check_in",
            "check_out",
        ]
