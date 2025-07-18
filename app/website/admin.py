from django.contrib import admin

from helpers.models.baseadmin_model import AdminBaseModel
from website.models import Company, Config, Department, Terminal, License


@admin.register(Company)
class CompanyDetailAdmin(AdminBaseModel):
    list_display = ["iid", "company_name", "address", "is_active"]

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return super().save_model(request, obj, form, change)
        return print(f"Invalid permissions to update model")


@admin.register(Config)
class AdvanceSettingAdmin(AdminBaseModel):
    list_display = ["key", "value", "config", "is_active", "created_by"]


@admin.register(Department)
class DepartmentAdmin(AdminBaseModel):
    list_display = ["iid", "name", "description", "is_active"]


@admin.register(Terminal)
class TerminalAdmin(AdminBaseModel):
    list_display = ["iid", "name", "terminal_ip"]


@admin.register(License)
class LicenseAdmin(AdminBaseModel):
    list_display = ["iid", "license_key", "start_date", "end_date", "status"]
