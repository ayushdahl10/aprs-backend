from django.core.management import BaseCommand
from payment.config import PAYMENT_CONFIG
from payment.models import PaymentMethod
from django.conf import settings
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    load base payment config
    """

    help = "load base payment config"

    def handle(self, **options):
        key = input("Enter payment name you wanna load: ")
        base_config = PAYMENT_CONFIG[key]
        base_config.update({"created_by": self.get_system_user()})
        PaymentMethod.objects.get_or_create(**base_config)
        print(f"Default Payment created successfully")

    def get_system_user(self):
        user_model = get_user_model()
        system_user = user_model.objects.get(username=settings.SYSTEM_USERNAME)
        return system_user
