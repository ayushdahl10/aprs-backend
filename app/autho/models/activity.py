from django.db import models

from autho.constant import AttendanceRequestType, LeaveStatusType, LeaveRequestType
from autho.constant import AttendanceStatusType
from helpers.mixins.constant import (
    WEBSITE_IID_STAFF_LOG,
    WEBSITE_IID_ATTEN_LOG,
    WEBSITE_IID_LEAVE_LOG,
)
from helpers.models.base_model import BaseModel


class Attendance(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_STAFF_LOG
    staff = models.ForeignKey("autho.Staff", on_delete=models.CASCADE, null=True)
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)
    status = models.CharField(
        choices=AttendanceStatusType.choices, default=AttendanceStatusType.PENDING
    )

    class Meta:
        verbose_name = "Attendance"

    def __str__(self):
        return f"{self.staff}"

    def delete(self, force=True, *args, **kwargs):
        return super().delete(force=force)


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
    status = models.CharField(
        choices=AttendanceStatusType.choices, default=AttendanceStatusType.PENDING
    )

    class Meta:
        verbose_name = "Attendance Request"

    def __str__(self):
        return f"{self.staff}"

    def delete(self, force=True, *args, **kwargs):
        return super().delete(force=force, *args, **kwargs)


class LeaveRequest(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_LEAVE_LOG
    staff = models.ForeignKey(
        "autho.Staff",
        on_delete=models.CASCADE,
        null=True,
        related_name="leave_request",
    )
    assigned_to = models.ManyToManyField(
        "autho.Staff",
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.TextField(max_length=500, null=False, blank=True, default="")
    status = models.CharField(
        choices=LeaveStatusType.choices, default=LeaveStatusType.PENDING
    )
    leave_type = models.CharField(
        choices=LeaveRequestType.choices, default=LeaveRequestType.ANNUAL_LEAVE
    )

    class Meta:
        verbose_name = "Leave Request"

    def __str__(self):
        return f"{self.staff}"

    def delete(self, force=True, *args, **kwargs):
        return super().delete(force=force)


class StaffActivityLogs(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_ATTEN_LOG
    staff = models.ForeignKey("autho.Staff", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Staff Activity Log"

    def __str__(self):
        return f"{self.staff}"
