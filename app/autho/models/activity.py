from django.db import models

from autho.constant import AttendanceRequestType
from helpers.mixins.constant import (
    WEBSITE_IID_STAFF_LOG,
    WEBSITE_IID_ATTEN_LOG,
    WEBSITE_IID_LEAVE_LOG,
)
from helpers.models.base_model import BaseModel


class Attendance(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_STAFF_LOG
    staff = models.ForeignKey("autho.Staff", on_delete=models.CASCADE, null=True)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Attendance"

    def __str__(self):
        return f"{self.staff}"


class AttendanceRequest(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_STAFF_LOG
    staff = models.ForeignKey(
        "autho.Staff",
        on_delete=models.CASCADE,
        null=True,
        related_name="attendance_requests_staff",
    )
    assigned_to = models.ManyToManyField(
        "autho.Staff",
        related_name="attendance_requests_assigned_to",
    )
    request_type = models.CharField(
        choices=AttendanceRequestType.choices,
        null=True,
    )
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(max_length=500, null=False, blank=True, default="")

    class Meta:
        verbose_name = "Attendance Request"

    def __str__(self):
        return f"{self.staff}"


class LeaveRequest(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_LEAVE_LOG
    staff = models.ForeignKey(
        "autho.Staff",
        on_delete=models.CASCADE,
        null=True,
        related_name="leave_requests_staff",
    )
    assigned_to = models.ManyToManyField(
        "autho.Staff",
        related_name="leave_requests_assigned_to",
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.TextField(max_length=500, null=False, blank=True, default="")
    
    class Meta:
        verbose_name = "Leave Request"

    def __str__(self):
        return f"{self.staff}"


class StaffActivityLogs(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_ATTEN_LOG
    staff = models.ForeignKey("autho.Staff", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Staff Activity Log"

    def __str__(self):
        return f"{self.staff}"
