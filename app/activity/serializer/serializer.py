from datetime import timedelta, datetime

from rest_framework import serializers

from activity.constant import AttendanceStatus
from autho.constant import AttendanceStatusType, LeaveStatusType
from autho.models import Attendance, AttendanceRequest
from autho.models import Staff, LeaveRequest
from helpers.base_serializer import BaseModelSerializer
from helpers.exceptions import NotFoundException
from helpers.serializer_fields import DetailRelatedField


class CalenderListSerializer(BaseModelSerializer):
    late_by = serializers.SerializerMethodField(read_only=True)
    early_by = serializers.SerializerMethodField(read_only=True)
    hours_worked = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)
    check_out = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    check_in = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

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
        if not obj.check_in:
            return obj.check_out.date()
        else:
            return obj.check_in.date()

    def get_late_by(self, obj):
        if obj.check_in:
            check_in_time = obj.check_in.time()
            shift_start_datetime = datetime.combine(
                datetime.today(), obj.staff.shift_start
            )
            shift_start_datetime = shift_start_datetime + timedelta(minutes=5)

            if check_in_time > shift_start_datetime.time():
                late_time_delta = (
                    datetime.combine(datetime.today(), check_in_time)
                    - shift_start_datetime
                )

                total_late_minutes = late_time_delta.total_seconds() / 60
                return int(total_late_minutes)
        return None

    def get_early_by(self, obj):
        if obj.check_out:
            check_out_time = obj.check_out.time()
            shift_end_datetime = datetime.combine(datetime.today(), obj.staff.shift_end)
            shift_end_datetime = shift_end_datetime - timedelta(minutes=5)

            if check_out_time < shift_end_datetime.time():
                early_time_delta = shift_end_datetime - datetime.combine(
                    datetime.today(), check_out_time
                )

                total_early_minutes = early_time_delta.total_seconds() / 60
                return int(total_early_minutes)
        return None

    def get_check_in(self, obj):
        if obj.check_in is None:
            return None
        return obj.check_in

    def get_check_out(self, obj):
        if obj.check_out is None:
            return None
        return obj.check_out

    def get_hours_worked(self, obj):
        if obj.check_in and obj.check_out:
            hours_worked = (obj.check_out - obj.check_in).total_seconds() / 3600
            hours_worked = round(hours_worked, 2)
            return f"{hours_worked} hrs"

    def get_status(self, obj):
        shift_start_datetime = datetime.combine(datetime.today(), obj.staff.shift_start)
        shift_end_datetime = datetime.combine(datetime.today(), obj.staff.shift_end)
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
    check_out = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    check_in = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
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


class AttendanceRequestCreateSerializer(BaseModelSerializer):
    reason = serializers.CharField(required=True)
    time = serializers.TimeField(required=True)
    date = serializers.DateField(required=True)

    class Meta:
        model = AttendanceRequest
        fields = [
            "iid",
            "request_type",
            "date",
            "time",
            "status",
            "reason",
        ]

    def validate(self, attrs):
        validated_data = attrs
        atten_request = self.Meta.model.objects.filter(
            staff=self.context.get("request").user.userdetail.staff,
            date=validated_data["date"],
            request_type=validated_data["request_type"],
        )
        if atten_request.exists():
            raise serializers.ValidationError(
                {"message": ["There is a request pending for this date already"]}
            )
        return validated_data

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["created_by"] = user
        validated_data["staff"] = user.userdetail.staff
        validated_data["status"] = AttendanceStatusType.PENDING
        attendance_request_instance = super().create(validated_data)
        attendance_request_instance.assigned_to.set(
            self.context.get("request").user.userdetail.staff.supervisor.all()
        )
        return attendance_request_instance


class AttendanceRequestlistSerializer(BaseModelSerializer):
    staff = DetailRelatedField(Staff, representation="get_basic_info")

    class Meta:
        model = AttendanceRequest
        fields = [
            "iid",
            "staff",
            "request_type",
            "date",
            "time",
            "reason",
            "is_active",
        ]


class AttendanceRequestChangeSerializer(BaseModelSerializer):
    staff = serializers.CharField(required=True)

    class Meta:
        model = AttendanceRequest
        fields = [
            "iid",
            "staff",
            "status",
        ]

    def validate_staff(self, value):
        try:
            staff = Staff.objects.get(iid=value)
        except Staff.DoesNotExist:
            raise NotFoundException("Staff cannot be found")
        return staff

    def validate(self, attrs):
        validated_data = attrs
        if validated_data["status"] == AttendanceStatusType.PENDING:
            raise serializers.ValidationError(
                {"message": "Please choose the status other than pending"}
            )
        return validated_data


class LeaveRequestListSerializer(BaseModelSerializer):
    staff = DetailRelatedField(Staff, representation="get_basic_info", read_only=True)
    start_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = LeaveRequest
        fields = [
            "iid",
            "staff",
            "start_datetime",
            "end_datetime",
            "leave_type",
            "is_active",
        ]


class LeaveRequestDetailSerializer(BaseModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = [
            "iid",
            "staff",
            "start_datetime",
            "end_datetime",
            "reason",
            "status",
        ]


class LeaveRequestCreateSerializer(BaseModelSerializer):
    reason = serializers.CharField(max_length=500, required=True, allow_blank=False)

    class Meta:
        model = LeaveRequest
        fields = [
            "iid",
            "start_datetime",
            "end_datetime",
            "reason",
            "leave_type",
        ]

    def validate(self, attrs):
        validated_data = attrs
        start_datetime = validated_data["start_datetime"]
        start_date_only = start_datetime.date()
        if self.Meta.model.objects.filter(
            start_datetime__date=start_date_only,
        ).exists():
            raise serializers.ValidationError(
                {"message": "There is already leave issued for this date"}
            )
        return validated_data

    def create(self, validated_data):
        validated_data["is_active"] = True
        validated_data["staff"] = self.context.get("request").user.userdetail.staff
        validated_data["created_by"] = self.context.get("request").user
        validated_data["status"] = LeaveStatusType.PENDING
        return super().create(validated_data)


class UpdateStatusLeaveRequestSerializer(BaseModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = [
            "iid",
            "staff",
            "status",
        ]
