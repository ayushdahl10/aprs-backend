from rest_framework import serializers

from autho.models import Attendance, LeaveRequest
from helpers.base_serializer import BaseModelSerializer


class CalenderListSerializer(BaseModelSerializer):
    late_check_in = serializers.SerializerMethodField(read_only=True)
    early_check_out = serializers.SerializerMethodField(read_only=True)
    check_in = serializers.SerializerMethodField(read_only=True)
    check_out = serializers.SerializerMethodField(read_only=True)
    absent = serializers.SerializerMethodField(read_only=True)
    hours_worked = serializers.SerializerMethodField(read_only=True)
    leave_approved = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "iid",
            "check_in",
            "check_out",
            "late_check_in",
            "early_check_out",
            "absent",
            "hours_worked",
            "leave_approved",
        ]

    def get_late_check_in(self, obj):
        check_in_time = obj.check_in.time()
        if check_in_time > obj.staff.shift_start:
            return obj.check_in
        return None

    def get_early_check_out(self, obj):
        check_out_time = obj.check_out.time()
        if check_out_time < obj.staff.shift_end:
            return obj.check_out
        return None

    def get_check_in(self, obj):
        return obj.check_in

    def get_check_out(self, obj):
        return obj.check_out

    def get_absent(self, obj):
        if not obj.check_in or not obj.check_out:
            return True
        else:
            return False

    def get_hours_worked(self, obj):
        if obj.check_in and obj.check_out:
            hours_worked = (obj.check_out - obj.check_in).total_seconds() / 3600
            hours_worked = round(hours_worked, 2)
            return f"{hours_worked} hrs"

    def get_leave_approved(self, obj):
        if LeaveRequest.objects.filter(is_approved=True, staff=obj.staff).exists():
            return True
        return False
