from helpers.base_serializer import BaseModelSerializer, BaseSerializer
from payment.models import PaymentMethod, PaymentLog, TransactionLog
from rest_framework import serializers
from autho.models import UserDetail
from payment.transaction import Esewa, Transaction
from payment.transaction.payment_handler import handle_payment_processing
from django.db import transaction


class PaymentInitializeSerializer(BaseModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    payment_method = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = TransactionLog
        fields = [
            "iid",
            "license",
            "amount",
            "username",
            "payment_method",
        ]

    def validate_payment_method(self, value):
        try:
            payment_method = PaymentMethod.objects.get(iid=value)
        except PaymentMethod.DoesNotExist:
            raise serializers.ValidationError("Invalid Payment method")
        return payment_method

    def validate_username(self, value):
        try:
            UserDetail.objects.get(user__username=value)
        except UserDetail.DoesNotExist:
            raise serializers.ValidationError("Invalid username")
        return value

    @transaction.atomic
    def initiate_transaction(self):
        pass
