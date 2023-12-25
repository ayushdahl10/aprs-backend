from django.contrib import admin
from django.http.request import HttpRequest
from property.models import Property, Tenant, LeaseInformation
from helpers.models.baseadmin_model import AdminBaseModel
from typing import Any


# Register your models here.
class LeaseInformationInline(admin.StackedInline):
    model = LeaseInformation
    extra = 1
    readonly_fields = [
        "created_by",
        "updated_by",
        "created_at",
        "is_deleted",
        "due_date",
    ]


class TenantInline(admin.StackedInline):
    model = Tenant
    extra = 1
    readonly_fields = ["created_by", "updated_by", "created_at", "is_deleted"]
    inlines = [LeaseInformationInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            db = kwargs.get("using")
            queryset = db_field.remote_field.model._default_manager.using(db).exclude(
                user__is_superuser=True,
            )
            kwargs["queryset"] = queryset
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Property)
class PropertyAdmin(AdminBaseModel):
    list_display = ["name", "company", "is_active"]
    inlines = [TenantInline]


@admin.register(Tenant)
class TenantAdmin(AdminBaseModel):
    list_display = ["title", "tenant_name", "property", "is_active"]
    inlines = [LeaseInformationInline]
    list_filter = ["property"]
    search_fields = ["title", "user__full_name", "property__name"]
    list_select_related = ["user"]
    ordering = ["user__full_name"]

    def tenant_name(self, value):
        return value.user.full_name

    def has_delete_permission(
        self, request: HttpRequest, obj: Any | None = ...
    ) -> bool:
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            db = kwargs.get("using")
            queryset = db_field.remote_field.model._default_manager.using(db).exclude(
                user__is_superuser=True,
            )
            kwargs["queryset"] = queryset
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(LeaseInformation)
class LeaseInformationAdmin(AdminBaseModel):
    list_display = ["tenant", "lease_type", "price", "tax", "lease_status", "due_date"]
    list_filter = ["tenant", "lease_type", "lease_status"]
    ordering = ["price"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
