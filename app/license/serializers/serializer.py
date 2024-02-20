from helpers.base_serializer import BaseModelSerializer
from license.models import License, Subscription
from helpers.serializer_fields import DetailRelatedField
from rest_framework import serializers
from django.utils import timezone


class LicenseDetailSerializer(BaseModelSerializer):
    subscription = DetailRelatedField(Subscription, representation="get_basic_info")
    due_date = serializers.DateField(source="end_date")
    name = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = License
        fields = [
            "iid",
            "name",
            "subscription",
            "license_key",
            "due_date",
            "message",
        ]

    def get_name(self, obj):
        return obj.client.name

    def get_message(self, obj):
        days_left = (obj.end_date - timezone.now().date()).days

        if obj.end_date < timezone.now().date():
            return (
                "Your payment is overdue. Please make the payment as soon as possible."
            )

        return f"You have {days_left} days left to make the payment. Feel free to pay in advance."
