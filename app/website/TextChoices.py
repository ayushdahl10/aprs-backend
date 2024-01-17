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
