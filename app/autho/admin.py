from django.contrib import admin

from autho.models import (
    UserDetail,
    UserActivityLog,
    Staff,
    Attendance,
    StaffActivityLogs,
    AttendanceRequest,
)
from helpers.models.baseadmin_model import AdminBaseModel


# Register your models here.
@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ["email", "full_name", "user_status", "user_type", "is_verified"]
    list_filter = ["user_type", "user__is_active"]
    search_fields = ["user__email"]

    def email(self, value):
        return value.user.email


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ["user", "login_count", "created_at"]
    sortable_by = ["login_count"]


@admin.register(Staff)
class StaffAdmin(AdminBaseModel):
    list_display = ["iid", "staff_id", "user", "is_active"]


@admin.register(Attendance)
class StaffLogsAdmin(AdminBaseModel):
    list_display = ["iid", "staff", "check_in", "check_out", "is_approved"]


@admin.register(StaffActivityLogs)
class StaffActivityLogAdmin(AdminBaseModel):
    list_display = ["iid", "staff", "created_at"]


@admin.register(AttendanceRequest)
class AttendanceRequestAdmin(AdminBaseModel):
    list_display = ["iid", "staff", "reason", "request_type"]
