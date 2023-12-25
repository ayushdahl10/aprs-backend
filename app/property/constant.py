from django.db.models import TextChoices


class PaymentTypeChoices(TextChoices):
    WEEKLY = ("week", ("Weekly"))
    MONTHLY = ("month", ("Monthly"))
    YEARLY = ("year", ("Yearly"))


class LeaseStatus(TextChoices):
    NOT_ACTIVE = ("not_active", ("Not Active"))
    ACTIVE = ("active", ("Active"))
    EXPIRED = ("expired", ("Expired"))
    REVOKED = ("revoked", ("Revoked"))
    LATE_BY = ("late", ("Late by"))
