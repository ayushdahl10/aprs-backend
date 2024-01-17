from datetime import datetime

from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action

from activity.filters import CalenderFilter, AttendanceRequestFilter
from activity.serializer import (
    CalenderListSerializer,
    CalenderDetailSerializer,
    AttendanceRequestCreateSerializer,
    AttendanceRequestlistSerializer,
    AttendanceRequestChangeSerializer,
    LeaveRequestCreateSerializer,
    LeaveRequestListSerializer,
    LeaveRequestDetailSerializer,
    UpdateStatusLeaveRequestSerializer,
)
from autho.constant import AttendanceRequestType
from autho.constant import AttendanceStatusType, LeaveStatusType
from autho.models import Attendance, Staff, AttendanceRequest, LeaveRequest
from helpers.exceptions import NotFoundException
from helpers.readony_viewset import ReadOnlyViewSet
from helpers.super_viewset import SuperViewset


class AttendanceAPI(ReadOnlyViewSet):
    queryset = Attendance.objects.filter(is_deleted=False, is_active=True)
    list_serializer = CalenderListSerializer
    detail_serializer = CalenderDetailSerializer
    filterset_class = CalenderFilter
    required_param = ["date_after", "date_before"]

    def list(self, request, *args, **kwargs):
        try:
            staff = Staff.objects.get(user__user=self.request.user)
        except Staff.DoesNotExist:
            raise NotFoundException("You are not a valid staff")
        queryset = self.get_queryset().filter(staff=staff)
        return super().list(request=request, queryset=queryset)


class AttendanceRequestAPI(SuperViewset):
    queryset = AttendanceRequest.objects.filter(is_deleted=False, is_active=True)
    create_serializer = AttendanceRequestCreateSerializer
    serializer_class = AttendanceRequestlistSerializer
    filterset_class = AttendanceRequestFilter
    force_delete = True

    def get_queryset(self):
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            status=AttendanceStatusType.PENDING,
            staff=self.request.user.userdetail.staff,
        )
        return super().list(request=request, queryset=queryset)

    @action(methods=["patch"], detail=True, url_path="update-request")
    def update_attendance_request(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = AttendanceRequestChangeSerializer(
            instance, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
            validated_data = serializer.validated_data
            if instance.request_type == AttendanceRequestType.CHECK_IN:
                fields = {
                    "staff": validated_data["staff"],
                    "status": validated_data["status"],
                    "created_by": self.request.user,
                    "check_in": datetime.combine(instance.date, instance.time),
                }
            else:
                fields = {
                    "staff": validated_data["staff"],
                    "status": validated_data["status"],
                    "created_by": self.request.user,
                    "check_out": datetime.combine(instance.date, instance.time),
                }
            try:
                atten = Attendance.objects.get(
                    Q(check_in__date=instance.date) | Q(check_out__date=instance.date),
                    staff=validated_data["staff"],
                )
                if instance.request_type == AttendanceRequestType.CHECK_IN:
                    atten.check_in = datetime.combine(instance.date, instance.time)
                else:
                    atten.check_out = datetime.combine(instance.date, instance.time)
                atten.status = validated_data["status"]
                atten.save()
            except Attendance.DoesNotExist:
                Attendance.objects.create(**fields)
        return self.on_api_success_response(
            f"Attendance request status changed successfully", status=200
        )

    @action(methods=["patch"], detail=True, url_path="bulk-update-request")
    def bulk_update_attendance_request(self, request, *args, **kwargs):
        data = request.data["status"]
        staffs = request.data["staff"]
        if len(staffs) <= 0 or staffs is None:
            return self.on_api_error_response(
                "Staff field cannot be empty",
                status.HTTP_400_BAD_REQUEST,
            )
        for staff in staffs:
            data["staff"] = staff
            instance = self.get_object()
            serializer = AttendanceRequestChangeSerializer(
                instance, data=data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
                validated_data = serializer.validated_data
                if instance.request_type == AttendanceRequestType.CHECK_IN:
                    fields = {
                        "staff": validated_data["staff"],
                        "status": validated_data["status"],
                        "created_by": self.request.user,
                        "check_in": datetime.combine(instance.date, instance.time),
                    }
                else:
                    fields = {
                        "staff": validated_data["staff"],
                        "status": validated_data["status"],
                        "created_by": self.request.user,
                        "check_out": datetime.combine(instance.date, instance.time),
                    }
                try:
                    atten = Attendance.objects.get(
                        Q(check_in__date=instance.date)
                        | Q(check_out__date=instance.date),
                        staff=validated_data["staff"],
                    )
                    if instance.request_type == AttendanceRequestType.CHECK_IN:
                        atten.check_in = datetime.combine(instance.date, instance.time)
                    else:
                        atten.check_out = datetime.combine(instance.date, instance.time)
                    atten.status = validated_data["status"]
                    atten.save()
                except Attendance.DoesNotExist:
                    Attendance.objects.create(**fields)
        return self.on_api_success_response(
            f"Attendance request status changed successfully", status=200
        )

    @action(methods=["get"], detail=False, url_path="staff-request")
    def get_staff_pending_request(self, request, *args, **kwargs):
        req_status = self.request.GET.get("status", None)
        queryset = self.get_queryset().filter(
            assigned_to=self.request.user.userdetail.staff
        )
        if req_status is not None:
            queryset = self.get_queryset().filter(status=req_status)
        if self.is_paginated:
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(
                queryset, request, view=self
            )
            serializer = AttendanceRequestlistSerializer(paginated_queryset, many=True)
            page_data, record_data = paginator.get_paginated_response(serializer.data)
            return self.on_api_success_pagination(
                page_data=page_data,
                records_data=record_data,
                status=status.HTTP_200_OK,
            )
        serializer = AttendanceRequestlistSerializer(queryset, many=True)
        return self.on_api_success_response(serializer.data, status=200)


class LeaveRequestAPI(SuperViewset):
    queryset = LeaveRequest.objects.all()
    create_serializer = LeaveRequestCreateSerializer
    list_serializer = LeaveRequestListSerializer
    detail_serializer = LeaveRequestDetailSerializer
    force_delete = True

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            Q(status=LeaveStatusType.PENDING)
            & Q(staff=self.request.user.userdetail.staff)
        )
        return super().list(request, queryset=queryset, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(iid=kwargs.get("iid"))
        except Exception:
            raise NotFoundException("Leave request not found")
        if instance.status == LeaveStatusType.PENDING:
            instance.delete(force=True)
            instance.save()
            return self.on_api_success_response("Leave deleted successfully", 200)
        return self.on_api_error_response(
            "Leave request not found", status=status.HTTP_404_NOT_FOUND
        )

    @action(methods=["patch"], detail=True, url_path="update-leave-request")
    def update_leave_request(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(iid=kwargs.get("iid"))
        except Exception:
            raise self.on_api_error_response(
                "Leave request not found",
                status=status.HTTP_404_NOT_FOUND,
            )
        update_status_serializer = UpdateStatusLeaveRequestSerializer(
            instance,
            data=self.request.data,
            partial=True,
            context={"request": self.request},
        )
        update_status_serializer.is_valid(raise_exception=True)
        update_status_serializer.save()
        return self.on_api_success_response(
            update_status_serializer.data, status=status.HTTP_200_OK
        )

    @action(methods=["get"], detail=False, url_path="check-request")
    def check_staff_request(self, request, *args, **kwargs):
        req_status = self.request.GET.get("status", None)
        queryset = self.get_queryset().filter(
            assigned_to=self.request.user.userdetail.staff
        )
        if req_status is not None:
            queryset = self.get_queryset().filter(status=req_status)
        if self.is_paginated:
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(
                queryset, request, view=self
            )
            serializer = LeaveRequestListSerializer(paginated_queryset, many=True)
            page_data, record_data = paginator.get_paginated_response(serializer.data)
            return self.on_api_success_pagination(
                page_data=page_data,
                records_data=record_data,
                status=status.HTTP_200_OK,
            )
        serializer = LeaveRequestListSerializer(queryset, many=True)
        return self.on_api_success_response(serializer.data, status=200)
