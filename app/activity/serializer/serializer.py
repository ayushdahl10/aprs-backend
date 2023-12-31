from datetime import timedelta, datetime

from rest_framework import serializers

from activity.constant import AttendanceStatus
from autho.constant import AttendanceStatusType, LeaveStatusType
from autho.models import Attendance, LeaveRequest
from helpers.base_serializer import BaseModelSerializer


class CalenderListSerializer(BaseModelSerializer):
    late_by = serializers.SerializerMethodField(read_only=True)
    early_by = serializers.SerializerMethodField(read_only=True)
    check_in = serializers.SerializerMethodField(read_only=True)
    check_out = serializers.SerializerMethodField(read_only=True)
    hours_worked = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "iid",
            "date",
            "check_in",
            "check_out",
            "late_by",
            "early_by",
            "hours_worked",
            "status",
        ]

    def get_date(self, obj):
        return obj.created_at.date()

    def get_late_by(self, obj):
        check_in_time = obj.check_in.time()
        shift_start_datetime = datetime.combine(datetime.today(), obj.staff.shift_start)
        shift_start_datetime = shift_start_datetime + timedelta(minutes=5)

        if check_in_time > shift_start_datetime.time():
            late_time_delta = (
                datetime.combine(datetime.today(), check_in_time) - shift_start_datetime
            )
            late_hours, remainder = divmod(late_time_delta.seconds, 3600)
            late_minutes, _ = divmod(remainder, 60)

            return f"{late_hours} hr {late_minutes} min"

        return None

    def get_early_by(self, obj):
        check_out_time = obj.check_out.time()
        shift_end_datetime = datetime.combine(datetime.today(), obj.staff.shift_end)
        shift_end_datetime = shift_end_datetime - timedelta(minutes=5)

        if check_out_time < shift_end_datetime.time():
            early_time_delta = shift_end_datetime - datetime.combine(
                datetime.today(), check_out_time
            )
            early_hours, remainder = divmod(early_time_delta.seconds, 3600)
            early_minutes, _ = divmod(remainder, 60)

            return f"{early_hours} hr and {early_minutes} min"

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
        if obj.check_in and obj.check_out:
            hours_worked = (obj.check_out - obj.check_in).total_seconds() / 3600
            hours_worked = round(hours_worked, 2)
            if hours_worked >= obj.staff.working_hours:
                return AttendanceStatus.PRESENT
        if LeaveRequest.objects.filter(
            status=LeaveStatusType.APPROVED, staff=obj.staff
        ).exists():
            return AttendanceStatus.LEAVE
        if obj.status == AttendanceStatusType.REJECTED:
            return AttendanceStatus.ABSENT
        elif obj.status == AttendanceStatusType.APPROVED:
            return AttendanceStatus.PRESENT
        elif obj.status == AttendanceStatusType.PENDING:
            return AttendanceStatus.PENDING_REQUEST
        return AttendanceStatus.ABSENT


class CalenderDetailSerializer(BaseModelSerializer):
    late_by = serializers.SerializerMethodField(read_only=True)
    early_by = serializers.SerializerMethodField(read_only=True)
    check_in = serializers.SerializerMethodField(read_only=True)
    check_out = serializers.SerializerMethodField(read_only=True)
    hours_worked = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    leave = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "iid",
            "check_in",
            "check_out",
            "late_by",
            "early_by",
            "hours_worked",
            "status",
            "leave",
        ]

    def get_late_by(self, obj):
        check_in_time = obj.check_in.time()
        shift_start_datetime = datetime.combine(datetime.today(), obj.staff.shift_start)
        shift_start_datetime = shift_start_datetime + timedelta(minutes=5)

        if check_in_time > shift_start_datetime.time():
            late_time_delta = (
                datetime.combine(datetime.today(), check_in_time) - shift_start_datetime
            )
            late_hours, remainder = divmod(late_time_delta.seconds, 3600)
            late_minutes, _ = divmod(remainder, 60)

            return f"{late_hours} hr {late_minutes} min"

        return None

    def get_early_by(self, obj):
        check_out_time = obj.check_out.time()
        shift_end_datetime = datetime.combine(datetime.today(), obj.staff.shift_end)
        shift_end_datetime = shift_end_datetime - timedelta(minutes=5)

        if check_out_time < shift_end_datetime.time():
            early_time_delta = shift_end_datetime - datetime.combine(
                datetime.today(), check_out_time
            )
            early_hours, remainder = divmod(early_time_delta.seconds, 3600)
            early_minutes, _ = divmod(remainder, 60)

            return f"{early_hours} hr and {early_minutes} min"

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
        if obj.check_in and obj.check_out:
            hours_worked = (obj.check_out - obj.check_in).total_seconds() / 3600
            hours_worked = round(hours_worked, 2)
            if hours_worked >= obj.staff.working_hours:
                return AttendanceStatus.PRESENT
        if LeaveRequest.objects.filter(
            status=LeaveStatusType.APPROVED, staff=obj.staff
        ).exists():
            return AttendanceStatus.LEAVE
        if (
            not obj.check_in
            or not obj.check_out
            or obj.status == AttendanceStatusType.REJECTED
        ):
            return AttendanceStatus.ABSENT
        elif (
            check_in_time < shift_start_datetime.time()
            and check_out_time > shift_end_datetime.time()
            and obj.status == AttendanceStatusType.APPROVED
        ):
            return AttendanceStatus.PRESENT
        elif (
            check_in_time > shift_start_datetime.time()
            or check_out_time < shift_end_datetime.time()
            or obj.status == AttendanceStatusType.PENDING
        ):
            return AttendanceStatus.PENDING_REQUEST
        return AttendanceStatus.PENDING_REQUEST

    def get_leave(self, obj):
        leave = LeaveRequest.objects.filter(
            is_deleted=False,
            is_active=True,
            start_datetime__gte=obj.check_in,
            end_datetime__lte=obj.check_in,
            status=LeaveStatusType.PENDING,
        )
        if leave.exists():
            return leave.first().reason
        return None
