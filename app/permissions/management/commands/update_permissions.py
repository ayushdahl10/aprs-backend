from django.core.management import BaseCommand
from django.db import transaction

from permissions.constant import ADMIN_USER, SUPER_ADMIN
from permissions.managepermission.users_permissions import (
    STAFF_API,
    DEPARTMENT_API,
    ATTENDANCE_API,
    COMPANY_API,
)
from permissions.models import Role, Permission


class Command(BaseCommand):
    """
    load builtin roles
    """

    help = "update roles permissions"

    def handle(self, **options):
        with transaction.atomic():
            update_user_roles(
                ADMIN_USER, [STAFF_API, DEPARTMENT_API, ATTENDANCE_API, COMPANY_API]
            )
            update_user_roles(
                SUPER_ADMIN, [STAFF_API, DEPARTMENT_API, ATTENDANCE_API, COMPANY_API]
            )
        print(f"role permissions updated successfully")


def update_user_roles(role_name, permission_name):
    allowed_permissions = permission_name
    try:
        role = Role.objects.get(name=role_name)
        role.permissions.clear()
    except Role.DoesNotExist:
        print(f"Role does not exists please load build in roles")
    for permission in allowed_permissions:
        for value in permission:
            prefix = value[0]
            type = value[1]
            permissions = Permission.objects.get(url_name=prefix, url_type=type)
            role.permissions.add(permissions)
    role.save()
