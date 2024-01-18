from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from helpers.mixins.helper import generate_random_string


class Command(BaseCommand):
    """
    create a default system user
    """

    help = "create a default system user"

    def handle(self, **options):
        username = input("Enter the username for the system user: ")

        try:
            self.create_default_system_user(username)
            self.stdout.write(
                self.style.SUCCESS(f"System user '{username}' created successfully")
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating system user: {e}"))

        print(f"system user created successfully")

    def create_default_system_user(self, username):
        user_model = get_user_model()
        systemuser = user_model.objects.create(username=username)
        systemuser.set_password(generate_random_string(10))
        systemuser.save()
