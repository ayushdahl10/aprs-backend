from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from autho.models import UserDetail
from helpers.base_serializer import BaseModelSerializer


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, allow_null=False)
    password = serializers.CharField(allow_null=False, required=True)
    confirm_password = serializers.CharField(allow_null=False, required=True)
    first_name = serializers.CharField(allow_null=False, required=True)
    last_name = serializers.CharField(allow_null=False, required=True)
    number = serializers.CharField(allow_null=True, required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "number",
        ]

    def validate(self, attrs):
        validated_data = attrs
        if validated_data["password"] != validated_data["confirm_password"]:
            raise serializers.ValidationError(
                {"message": "Confirm password and password didnt match"}
            )
        return validated_data


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, allow_null=False)
    password = serializers.CharField(write_only=True, allow_null=False)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        try:
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.userdetail.is_verified == False:
                    raise serializers.ValidationError(
                        "please contact the site admin to activate your account"
                    )
                if user.is_authenticated:
                    try:
                        token = Token.objects.get(user=user)
                        attrs["token"] = token.key
                    except Token.DoesNotExist:
                        token = Token.objects.create(user=user)
                        attrs["token"] = token.key
            else:
                raise serializers.ValidationError(
                    {
                        "message": "Invalid Password",
                        "status_code": 400,
                    }
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "message": "Invalid Email",
                    "status_code": 400,
                }
            )

        return attrs


class UserDetailSerializer(BaseModelSerializer):
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "iid",
            "email",
            "first_name",
            "last_name",
        ]
