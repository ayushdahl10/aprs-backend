from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

WEBSITE_GROUP_NAME = "RegisteredUser"
STAFF = "Staff"
ADMIN = "Admin"


class UserStatusChoices(TextChoices):
    ACTIVE = (
        "active",
        _("Active"),
    )
    SUSPENDED = (
        "suspended",
        _("Suspended"),
    )
    BANNED = "banned", _("Banned")


class UserTypeChoices(TextChoices):
    OWNER = ("owner", _("Owner"))
    TENANT = ("tenant", _("Tenant"))
    STAFF = ("staff", _("Staff"))
    CUSTOMER = ("customer", _("Customer"))
    ADMIN = ("admin", _("Admin"))


class AttendanceRequestType(TextChoices):
    CHECK_IN = ("in", _("Check In"))
    CHECK_OUT = ("out", _("Check Out"))


class AttendanceStatusType(TextChoices):
    REJECTED = ("rejected", _("Rejected"))
    APPROVED = ("approved", _("Approved"))
    PENDING = ("pending", _("Pending"))
    LEAVE_ACCEPTED = ("leave", _("Leave"))


class LeaveStatusType(TextChoices):
    REJECTED = ("rejected", _("Rejected"))
    APPROVED = ("approved", _("Approved"))
    PENDING = ("pending", _("Pending"))


class LeaveRequestType(TextChoices):
    SICK_LEAVE = ("sick_leave", _("Sick Leave"))
    ANNUAL_LEAVE = ("annual_leave", _("Annual Leave"))
    FIELD_LEAVE = ("field_leave", _("Field Leave"))
    MOURNING_LEAVE = ("mourning_leave", _("Mourning Leave"))
    PARENTAL_LEAVE = ("parental_leave", _("Parental Leave"))
