from django.db.models import TextChoices


class PaymentStatus(TextChoices):
    PENDING = "pending", ("Pending")
    COMPLETE = "complete", ("Complete")
    CANCEL = "cancel", ("Cancel")
    EXPIRED = "expired", ("Expired")
