from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.models import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from autho.constant import (
    WEBSITE_GROUP_NAME,
)
from autho.models import UserDetail
from autho.serializers import (
    RegisterUserSerializer,
    LoginSerializer,
    UserDetailSerializer,
)
from helpers.mixins.api_mixins import APIMixin
from helpers.mixins.helper import generate_random_string


class RegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer._validated_data
            email = validated_data["email"]
            password = validated_data["password"]
            first_name = validated_data["first_name"]
            last_name = validated_data["last_name"]
            number = validated_data["number"]
            try:
                user = User.objects.get(email=email)
                return Response({"message": ["Email already exists"], "status": 404})
            except User.DoesNotExist:
                group = Group.objects.get(name=WEBSITE_GROUP_NAME)
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
                    "full_name": first_name + last_name,
                    "user": user,
                    "number": number,
                    "is_email_verified": False,
                    "is_verified": True,
                }
                UserDetail.objects._save(**fields)
            return Response(
                {
                    "message": "User created Succesfully",
                    "status": status.HTTP_201_CREATED,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.CreateAPIView, APIMixin):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validate_data = serializer.validated_data
            return self.on_api_success_response(
                data={
                    "token": validate_data["token"],
                },
                status=status.HTTP_200_OK,
            )
        return self.on_api_error_response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class UserDetailAPI(generics.RetrieveAPIView):
    queryset = UserDetail.objects.filter()
    serializer_class = UserDetailSerializer

    def get_object(self):
        try:
            user_detail = self.get_queryset().get(user=self.request.user)
            return user_detail
        except ObjectDoesNotExist:
            raise Http404("UserDetail does not exist for the specified user.")

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response(
                {"msg": "Cannot get data", "status": 404},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"msg": instance.user.email, "status": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )


class ValidateTokenAPI(generics.ListAPIView):
    queryset = User.objects.none()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        user_detail = {
            "email": user.email,
            "role": user.groups.all().values_list("name", flat=True),
        }
        return Response(user_detail, status=status.HTTP_200_OK)
