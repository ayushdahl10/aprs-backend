from django.core.management import BaseCommand
from django.db import transaction

from permissions.managepermission.map_permission import (
    GET_ALL_PERMISSION,
)
from permissions.constant import PRIMARY_ROLES
from permissions.models import Permission


@transaction.atomic
def create_api_permission():
    Permission.objects.all().delete()
    for permissions in GET_ALL_PERMISSION:
        for permission in permissions:
            permissions = Permission.objects.get_or_create(
                url_name=permission[0], url_type=permission[1]
            )
    print(f"permission loaded successfully")


class Command(BaseCommand):
    """
    load builtin roles
    """

    help = "load builtin roles"

    def handle(self, **options):
        create_api_permission()
