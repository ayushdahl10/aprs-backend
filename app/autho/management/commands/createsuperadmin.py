from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from helpers.mixins.helper import generate_random_string
from autho.models import UserDetail
from permissions.models import Role
from permissions.constant import SUPER_ADMIN
from autho.constant import UserTypeChoices

class Command(BaseCommand):
    """
    create a super admin user
    """

    help = "create a super admin"

    def handle(self, **options):
        username = input("Enter the username for the super admin: ")
        email=input("Enter Email for super admin")
        password=input("Enter password for super admin")
        try:
            role=Role.objects.get(name=SUPER_ADMIN)
        except Role.DoesNotExist:
            raise self.stderr.write("Super Admin role does not exists")
        user={
            "username":username,
            "email":email,
            "password":password,
            "role":role
        }
        userdetail={
            "fullname":email,
            "user_type":UserTypeChoices.ADMIN,
            "is_verified":True
        }

        fields={
            "user":user,
            "detail":userdetail
        }

        try:
            self.create_default_system_user(**fields,**fields)
            self.stdout.write(
                self.style.SUCCESS(f"System user '{username}' created successfully")
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating system user: {e}"))

        print(f"system user created successfully")

    def create_default_system_user(self, **kwargs):
        user=kwargs.get("user")
        detail=kwargs.get("detail")
        user_model = get_user_model()
        systemuser = user_model.objects.create(**user)
        systemuser.set_password(user.get("password"))
        systemuser.save()
        UserDetail.objects.create(**detail)
