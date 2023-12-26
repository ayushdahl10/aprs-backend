from django.contrib.auth.models import User
from django.db import models

from autho.constant import UserStatusChoices, UserTypeChoices
from autho.manager.manager import BaseAuthManager


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=500, null=True, blank=True, default="")
    number = models.CharField(max_length=15, null=False, blank=True)
    address = models.CharField(max_length=126, null=True, blank=True)
    dob = models.DateField(null=True, help_text="Enter date of birth")
    user_status = models.CharField(
        choices=UserStatusChoices.choices, default=UserStatusChoices.ACTIVE
    )
    user_type = models.CharField(
        choices=UserTypeChoices.choices, default=UserTypeChoices.CUSTOMER
    )
    profile_pic = models.ImageField(
        null=True, blank=True, help_text="Upload your profile picture"
    )
    is_email_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = BaseAuthManager()

    def __str__(self) -> str:
        return f"{self.user.email}"
