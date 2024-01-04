from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.db import transaction

from autho.constant import UserTypeChoices
from autho.models import UserDetail
from permissions.constant import SUPER_ADMIN
from permissions.models import Role


class Command(BaseCommand):
    """
    create a super admin user
    """

    help = "create a super admin"

    def handle(self, **options):
        username = input("Enter the username for the super admin: ")
        email = input("Enter Email for super admin: ")
        password = input("Enter password for super admin: ")
        with transaction.atomic():
            try:
                group = Group.objects.get(name=SUPER_ADMIN)
            except Role.DoesNotExist:
                raise self.stderr.write("Super Admin role does not exists")
            user = {
                "username": username,
                "email": email,
                "password": password,
            }
            userdetail = {
                "user": None,
                "full_name": email,
                "user_type": UserTypeChoices.ADMIN,
                "is_verified": True,
            }

            fields = {"user": user, "detail": userdetail, "groups": group}

            try:
                self.create_default_system_user(**fields)
                self.stdout.write(
                    self.style.SUCCESS(f"System user '{username}' created successfully")
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error creating system user: {e}"))

            print(f"super admin created successfully")

    def create_default_system_user(self, **kwargs):
        user = kwargs.get("user")
        detail = kwargs.get("detail")
        groups = kwargs.get("groups")
        user_model = get_user_model()
        systemuser = user_model.objects.create(**user)
        systemuser.set_password(user.get("password"))
        systemuser.groups.add(groups)
        systemuser.save()
        detail.update({"user": systemuser})
        UserDetail.objects.create(**detail)
