from django.db.models import TextChoices


class AttendanceStatus(TextChoices):
    LEAVE = (
        "leave",
        "Leave",
    )
    ABSENT = "absent", "Absent"
    PRESENT = (
        "present",
        "Present",
    )
    PENDING_REQUEST = (
        "pending_request",
        "Pending Request",
    )
