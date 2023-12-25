from django.core.management import BaseCommand
from permissions.constant import PRIMARY_ROLES
from django.contrib.auth.models import Group


class Command(BaseCommand):
    """
    load builtin roles
    """

    help = "load builtin roles"

    def handle(self, **options):
        from permissions.models import Role

        builtin_roles = PRIMARY_ROLES
        self.create_group_and_role()
        for somerole in builtin_roles:
            try:
                Role.objects.get(name=somerole)
            except Role.DoesNotExist:
                Role.objects.create(name=somerole)

        print(f"Role updated successfully")

    def create_group_and_role(self):
        for name in PRIMARY_ROLES:
            Group.objects.get_or_create(name=name)
