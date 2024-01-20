from helpers.super_viewset import SuperViewset
from payment.models import PaymentMethod, PaymentLog
from rest_framework.decorators import action
from payment.serializers import PaymentInitializeSerializer


class PayAPI(SuperViewset):
    queryset = PaymentLog.objects.none()
    disallowed_methods = ["list", "create", "retrieve", "update", "partial_update"]

    @action(methods=["post"], detail=False, url_path="e-pay")
    def pay_subscription(self, request, *args, **kwargs):
        data = request.data

        transaction_serializer = PaymentInitializeSerializer(
            data=request.data, context={"request": self.request}
        )
        transaction_serializer.is_valid(raise_exception=True)
        return self.on_api_success_response("This method is allowed", status=200)
