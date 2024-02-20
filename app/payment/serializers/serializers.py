from helpers.base_serializer import BaseModelSerializer, BaseSerializer
from payment.models import PaymentMethod, PaymentLog, TransactionLog
from rest_framework import serializers
from autho.models import UserDetail
from payment.transaction.payment_handler import handle_payment_processing
from django.db import transaction
from license.models import License
import urllib.parse
from django.utils import timezone
from datetime import timedelta
from payment.constant import PaymentStatus
from helpers.mixins.helper import generate_random_string
from website.TextChoices import LicenseStatus, LicenseType, BillingType


class PaymentInitializeSerializer(BaseModelSerializer):
    payment_method = serializers.CharField(required=True, allow_blank=False)
    success_url = serializers.URLField(required=True, allow_blank=False)
    failure_url = serializers.URLField(required=True, allow_blank=False)

    class Meta:
        model = TransactionLog
        fields = [
            "iid",
            "payment_method",
            "success_url",
            "failure_url",
        ]

    def validate_payment_method(self, value):
        try:
            payment_method = PaymentMethod.objects.get(iid=value)
        except PaymentMethod.DoesNotExist:
            raise serializers.ValidationError("Invalid Payment method")
        return payment_method

    def validate(self, attrs):
        validated_data = attrs
        validated_data["license"] = License.objects.filter(
            client__userdetail__user=self.context.get("request").user
        ).first()
        if validated_data["license"] is None:
            raise serializers.ValidationError(
                "Please assign userdetail in client details"
            )
        # convert rs to paisa
        validated_data["amount"] = validated_data["license"].subscription.price * 100
        return validated_data

    @transaction.atomic
    def initiate_transaction(self):
        transaction_uuid = generate_random_string(16)
        payment_initiate_response = handle_payment_processing(
            "initiate",
            self.validated_data["payment_method"],
            **{
                "amount": self.validated_data["amount"]
                / 100,  # conver this paisa in rs
                "success_url": self.validated_data["success_url"],
                "failure_url": self.validated_data["failure_url"],
                "transaction_uuid": transaction_uuid,
            },
        )
        parsed_url = urllib.parse.urlparse(payment_initiate_response)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        bookingId = query_params["bookingId"][0]
        return payment_initiate_response, bookingId, transaction_uuid


class CreateTransactionLogSerializer(BaseModelSerializer):
    payment_method = serializers.CharField(write_only=True)
    license = serializers.CharField(write_only=True)

    class Meta:
        model = TransactionLog
        fields = [
            "iid",
            "amount",
            "payment_method",
            "lookup_id",
            "license",
            "response",
        ]

    def validate_payment_method(self, value):
        try:
            payment_method = PaymentMethod.objects.get(iid=value)
        except PaymentMethod.DoesNotExist:
            raise serializers.ValidationError("Invalid Payment method")
        return payment_method

    def validate_license(self, value):
        try:
            license = License.objects.get(iid=value, is_active=True, is_deleted=False)
        except License.DoesNotExist:
            raise serializers.ValidationError("Invalid License method")
        return license

    def create(self, validated_data):
        license = validated_data["license"]
        validated_data["created_by"] = self.context.get("request").user
        validated_data["expire_at"] = timezone.now() + timedelta(minutes=30)
        validated_data["subscription_date"] = license.end_date + timedelta(days=1)
        return super().create(validated_data)


class VerifyPaymentSerializer(BaseModelSerializer):
    verification_code = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = TransactionLog
        fields = ["iid", "verification_code"]

    def validate_verification_code(self, value):
        if self.Meta.model.objects.filter(lookup_id=value).exists():
            return value
        raise serializers.ValidationError("Invalid Verification code")

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        self.transaction = self.Meta.model.objects.get(
            lookup_id=validated_data["verification_code"]
        )
        return validated_data

    @transaction.atomic
    def verify_transaction(self, verification_code):
        transaction_uuid = verification_code
        payment_verification_response = handle_payment_processing(
            "verify",
            self.transaction.payment_method,
            **{
                "amount": self.transaction.amount,
                "transaction_uuid": transaction_uuid,
            },
        )
        if payment_verification_response == PaymentStatus.COMPLETE:
            self.transaction_status = PaymentStatus.COMPLETE
        elif payment_verification_response == PaymentStatus.CANCEL:
            self.transaction_status = PaymentStatus.CANCEL
        elif payment_verification_response == PaymentStatus.EXPIRED:
            self.transaction_status = PaymentStatus.EXPIRED

    # update transaction status and license end time
    def update_transaction(self):
        self.transaction.status = self.transaction_status
        self.transaction.updated_by = self.context.get("request").user.email
        self.transaction.save()

    def update_license_enddate(self):
        license = self.transaction.license
        current_end_date = license.end_date
        next_end_date = current_end_date + self.__get_days_count()
        license.end_date = next_end_date
        license.save()

    def __get_days_count(self):
        from dateutil.relativedelta import relativedelta

        billing_cycle = self.transaction.license.subscription.billing_type
        if billing_cycle == BillingType.MONTHLY:
            return relativedelta(months=1)
        if billing_cycle == BillingType.QUARTERLY:
            return relativedelta(months=3)
        if billing_cycle == BillingType.SEMI_ANNUAL:
            return relativedelta(months=6)
        if billing_cycle == BillingType.YEARLY:
            return relativedelta(years=1)
