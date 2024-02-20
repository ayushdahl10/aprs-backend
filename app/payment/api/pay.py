from helpers.super_viewset import SuperViewset
from payment.models import PaymentMethod, PaymentLog
from rest_framework.decorators import action
from payment.serializers import (
    PaymentInitializeSerializer,
    CreateTransactionLogSerializer,
    VerifyPaymentSerializer,
)
from rest_framework import status


class PayAPI(SuperViewset):
    queryset = PaymentLog.objects.none()
    disallowed_methods = ["list", "create", "retrieve", "update", "partial_update"]

    @action(methods=["post"], detail=False, url_path="e-pay")
    def pay_subscription(self, request, *args, **kwargs):
        transaction_serializer = PaymentInitializeSerializer(
            data=request.data, context={"request": self.request}
        )
        transaction_serializer.is_valid(raise_exception=True)
        (
            return_url,
            bookingId,
            transaction_uuid,
        ) = transaction_serializer.initiate_transaction()
        fields = {
            "lookup_id": transaction_uuid,
            "amount": transaction_serializer.validated_data["amount"],
            "payment_method": transaction_serializer.validated_data[
                "payment_method"
            ].iid,
            "license": transaction_serializer.validated_data["license"].iid,
            "response": {
                "bookingId": bookingId,
            },
        }
        create_transaction_log = CreateTransactionLogSerializer(
            data=fields, context={"request": self.request}
        )
        create_transaction_log.is_valid(raise_exception=True)
        create_transaction_log.save()
        return self.on_api_success_response(
            {
                "return_url": return_url,
                "transaction_uuid": transaction_uuid,
            },
            status=status.HTTP_200_OK,
        )

    @action(methods=["post"], detail=False, url_path="payment_verification")
    def verify_payment(self, request, *args, **kwargs):
        data = self.request.data
        verify_payment = VerifyPaymentSerializer(
            data=data, context={"request": self.request}
        )
        verify_payment.is_valid(raise_exception=True)
        verify_payment.verify_transaction(
            verification_code=verify_payment.data.get("verification_code")
        )
        verify_payment.update_transaction()
        verify_payment.update_license_enddate()
        return self.on_api_success_response("Payment verification success", status=200)
