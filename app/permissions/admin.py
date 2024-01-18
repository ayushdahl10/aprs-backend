from django.contrib import admin

from helpers.models.baseadmin_model import AdminBaseModel
from permissions.models import Permission, Role, AttendanceRoleAccess


# Register your models here.


@admin.register(Permission)
class APIPermissionAdmin(admin.ModelAdmin):
    list_display = ("url_name", "url_type")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(AttendanceRoleAccess)
class AttendanceRoleAccessAdmin(AdminBaseModel):
    list_display = ("iid", "role", "is_active")
