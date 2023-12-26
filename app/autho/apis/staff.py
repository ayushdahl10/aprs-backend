from helpers.super_viewset import SuperViewset
from autho.models import Staff
from autho.serializers import CreateStaffSerializer, RegisterUserSerializer,ListStaffSerializer
from autho.models import User, UserDetail, Group
from rest_framework.response import Response
from autho.constant import (
    ADMIN,
)
from helpers.mixins.helper import generate_random_string
from django.db import transaction
from rest_framework.permissions import AllowAny
from autho.constant import UserTypeChoices


class StaffAPI(SuperViewset):
    queryset = Staff.objects.filter()
    create_update_serializer = CreateStaffSerializer
    list_serializer=ListStaffSerializer

    def create(self, request, *args, **kwargs):
        user_detail = self.request.data["user_detail"]
        staff_detail = self.request.data["staff_detail"]
        user_serializer = RegisterUserSerializer(
            data=user_detail, context={"request": self.request}
        )
        user_serializer.is_valid(raise_exception=True)
        validated_data = user_serializer._validated_data
        email = validated_data["email"]
        password = validated_data["password"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        number = validated_data["number"]
        with transaction.atomic():
            try:
                user = User.objects.get(email=email)
                return Response({"message": ["Email already exists"], "status": 404})
            except User.DoesNotExist:
                group = Group.objects.get(name=ADMIN)
                user = User.objects.create(
                    username=generate_random_string(12),
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.groups.add(group)
                user.set_password(password)
                user.save()
                fields = {
                    "user": user,
                    "number": number,
                    "is_email_verified": False,
                    "is_verified": True,
                    "user_type": UserTypeChoices.STAFF,
                }
                instance = UserDetail.objects._save(**fields)
            staff_detail["user"] = instance.id
            staff_serializer = CreateStaffSerializer(
                data=staff_detail, context={"request": self.request}
            )
            staff_serializer.is_valid(raise_exception=True)
            staff_serializer.save()
        return self.on_api_success_response("Staff created successfully", status=201)


