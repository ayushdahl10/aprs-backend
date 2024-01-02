from datetime import datetime

from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action

from activity.filters import CalenderFilter
from activity.serializer import (
    CalenderListSerializer,
    CalenderDetailSerializer,
    AttendanceRequestCreateSerializer,
    AttendanceRequestlistSerializer,
    AttendanceRequestChangeSerializer,
)
from autho.constant import AttendanceRequestType
from autho.constant import AttendanceStatusType
from autho.models import Attendance, Staff, AttendanceRequest
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
        except Staff.DoesNotExists:
            raise NotFoundException("You are not a valid staff")
        queryset = self.get_queryset().filter(staff=staff)
        return super().list(request=request, queryset=queryset)


class AttendanceRequestAPI(SuperViewset):
    queryset = AttendanceRequest.objects.filter(is_deleted=False, is_active=True)
    create_update_serializer = AttendanceRequestCreateSerializer
    serializer_class = AttendanceRequestlistSerializer
    force_delete = True

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

    @action(methods=["get"], detail=False, url_path="staff-request")
    def get_staff_pending_request(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            assigned_to=self.request.user.userdetail.staff,
            status=AttendanceStatusType.PENDING,
        )
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
