from datetime import timedelta, datetime

from rest_framework import serializers

from autho.constant import AttendanceStatusType
from autho.models import Attendance, LeaveRequest
from helpers.base_serializer import BaseModelSerializer


class CalenderListSerializer(BaseModelSerializer):
    late_check_in = serializers.SerializerMethodField(read_only=True)
    early_check_out = serializers.SerializerMethodField(read_only=True)
    check_in = serializers.SerializerMethodField(read_only=True)
    check_out = serializers.SerializerMethodField(read_only=True)
    hours_worked = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "iid",
            "check_in",
            "check_out",
            "late_check_in",
            "early_check_out",
            "hours_worked",
            "status",
        ]

    def get_late_check_in(self, obj):
        check_in_time = obj.check_in.time()
        shift_start_datetime = datetime.combine(datetime.today(), obj.staff.shift_start)
        shift_start_datetime = shift_start_datetime + timedelta(minutes=5)
        if check_in_time > shift_start_datetime.time():
            return obj.check_in
        return None

    def get_early_check_out(self, obj):
        check_out_time = obj.check_out.time()
        shift_end_datetime = datetime.combine(datetime.today(), obj.staff.shift_end)
        shift_end_datetime = shift_end_datetime - timedelta(minutes=5)
        if check_out_time < shift_end_datetime.time():
            return obj.check_out
        return None

    def get_check_in(self, obj):
        return obj.check_in

    def get_check_out(self, obj):
        return obj.check_out

    def get_hours_worked(self, obj):
        if obj.check_in and obj.check_out:
            hours_worked = (obj.check_out - obj.check_in).total_seconds() / 3600
            hours_worked = round(hours_worked, 2)
            return f"{hours_worked} hrs"

    def get_status(self, obj):
        check_in_time = obj.check_in.time()
        check_out_time = obj.check_out.time()
        shift_start_datetime = datetime.combine(datetime.today(), obj.staff.shift_start)
        shift_end_datetime = datetime.combine(datetime.today(), obj.staff.shift_end)
        shift_start_datetime = shift_start_datetime + timedelta(minutes=5)
        shift_end_datetime = shift_end_datetime - timedelta(minutes=5)
        if LeaveRequest.objects.filter(is_approved=True, staff=obj.staff).exists():
            return "leave"
        if (
            not obj.check_in
            or not obj.check_out
            or obj.status == AttendanceStatusType.REJECTED
        ):
            return "absent"
        elif (
            check_in_time < shift_start_datetime.time()
            and check_out_time > shift_end_datetime.time()
            and obj.status == AttendanceStatusType.APPROVED
        ):
            return "present"
        elif (
            check_in_time > shift_start_datetime.time()
            or check_out_time < shift_end_datetime.time()
            or obj.status == AttendanceStatusType.PENDING
        ):
            return "pending approval"
        return "pending"
