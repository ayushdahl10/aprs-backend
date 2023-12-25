from django.core.management import BaseCommand
from website.models import Config
from website.constant.base_config import BASE_CONFIG
from django.conf import settings
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    load base config
    """

    help = "load base config"

    def handle(self, **options):
        key = input("Enter base config name: ")
        base_config = BASE_CONFIG[key]
        base_config.update({"created_by": self.get_system_user()})
        Config.objects.get_or_create(**base_config)
        print(f"Config created successfully")

    def get_system_user(self):
        user_model = get_user_model()
        system_user = user_model.objects.get(username=settings.SYSTEM_USERNAME)
        return system_user
