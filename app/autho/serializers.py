from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from autho.models import UserActivityLog, Staff
from website.models import Department


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
                if user.is_authenticated:
                    try:
                        token = Token.objects.get(user=user)
                        attrs["token"] = token.key
                    except Token.DoesNotExist:
                        token = Token.objects.create(user=user)
                        attrs["token"] = token.key
            else:
                raise serializers.ValidationError(
                    {"msg": "Invalid Password", "status_code": 400}
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"msg": "Invalid Email", "status_code": 400}
            )

        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
        ]


class CreateStaffSerializer(serializers.ModelSerializer):
    joined_date = serializers.DateField(required=True, allow_null=False)
    shift_start = serializers.TimeField(required=True, allow_null=False)
    shift_end = serializers.TimeField(required=True, allow_null=False)
    position = serializers.CharField(required=True)
    working_hours = serializers.CharField(required=True)
    staff_id = serializers.CharField(required=True)
    department = serializers.SlugRelatedField(
        slug_field="iid",
        queryset=Department.objects.filter(is_active=True,is_deleted=False),
        required=True
    )

    class Meta:
        model = Staff
        fields = [
            "user",
            "joined_date",
            "shift_start",
            "shift_end",
            "working_hours",
            "position",
            "staff_id",
            "department",
        ]


class ListStaffSerializer(serializers.ModelSerializer):
    email=serializers.CharField(source="user.user.email",read_only=True)
    first_name=serializers.CharField(source="user.user.first_name",read_only=True)
    last_name=serializers.CharField(source="user.user.last_name",read_only=True)
    number=serializers.CharField(source="user.number",read_only=True)
    address=serializers.CharField(source="user.address",read_only=True)
    class Meta:
        model = Staff
        fields = [
            "email",
            "first_name",
            "last_name",
            "number",
            "address",
            "joined_date",
            "shift_start",
            "shift_end",
            "working_hours",
            "position",
            "staff_id",
        ]
    