from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliverChoices(models.TextChoices):
    IN_PROCESS = "process", _("In Process")
    STARTED = "started", _("Started")
    COMPLETE = "complete", _("Complete")
    CANCEL = "cancel", _("Cancel")


class LicenseStatus(models.TextChoices):
    INACTIVE = "in_active", _("In Active")
    ACTIVE = "active", _("Active")
    EXPIRED = "expired", _("Expired")
    REVOKED = "revoked", _("Revoked")


class LicenseType(models.TextChoices):
    REGULAR = "regular", _("Regular")
    STANDARD = "standard", _("Standard")
    PREMIUM = "premiun", _("Premium")


class SubscriptionType(models.TextChoices):
    MONTHLY = "monthly", _("Monthly")
    YEARLY = "yearly", _("Yearly")
    QUARTERLY = "quarterly", _("Quarterly")
    SEMI_ANNUAL = "semi_annual", _("Semi-Annual")
