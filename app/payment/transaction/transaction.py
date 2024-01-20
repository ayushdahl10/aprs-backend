from payment.transaction import Transaction
from website.models import Config
from helpers.mixins.helper import generate_random_string
from helpers.exceptions import InvalidOperationException
import logging
from django.utils import timezone
from datetime import timedelta
import requests


class Esewa(Transaction):
    def __init__(self) -> None:
        super().__init__()

    def get_config(self):
        try:
            config = Config.objects.get(key="esewa_config", app=APP_NAME).config
            paymenty_endpoint = config.get("payment-initiate")
            payment_verify_endpoint = config.get("payment-verification")
            sandbox_endpoint = config.get("sandbox-endpoint")
            live_endpoint = config.get("live-endpoint")
            if (
                not paymenty_endpoint
                or not payment_verify_endpoint
                or not sandbox_endpoint
                or not live_endpoint
            ):  # noqa
                raise InvalidOperationException("Invalid Esewa Config")
            return config
        except Config.DoesNotExist:
            raise InvalidOperationException(
                "Error processing payment. Please try again later."
            )

    def get_base_url(self, sandbox_mode):
        if sandbox_mode:
            return self.config.get("sandbox-endpoint")
        return self.config.get("live-endpoint")

    def payment_initiate(self, payment_method, payment_data, *args, **kwargs):
        payment_initiate_url = self.config.get("payment-initiate")
        merchant_id = payment_method.config.get("merchant")
        sandbox_mode = payment_method.sandbox_mode
        amount = payment_data["amount"] / 100
        success_link = kwargs.get("success_url")
        fail_link = kwargs.get("failure_url")
        pidx = generate_random_string(20)

        if not merchant_id:
            logging.error(
                msg=f"[esewa-payment-initiate] Invalid merchant id({merchant_id})"
            )
            raise InvalidOperationException(
                "Error processing payment. Please try again later."
            )

        url = self.get_base_url(sandbox_mode)
        if payment_initiate_url.startswith("/"):
            payment_initiate_url = payment_initiate_url[1:]
        url = f"{url}{payment_initiate_url}"
        payment_url = f"{url}?amt={amount}&tAmt={amount}&pdc=0&psc=0&scd={merchant_id}&pid={pidx}&txAmt=0&su={success_link}&fu={fail_link}"
        fields = {
            "payment_url": payment_url,
            "payment_expiry": timezone.now() + timedelta(minutes=5),
            "pidx": pidx,
        }
        return fields

    def payment_verify(self, payment_method, **kwargs):
        sandbox_mode = payment_method.sandbox_mode
        payment_lookup_url = self.config.get("payment-verification")
        merchant_id = payment_method.config.get("merchant")
        verification_code = kwargs.get("verification_code")
        pid = kwargs.get("pidx")
        amount = kwargs.get("transaction").amount
        d = {
            "amt": amount / 100,
            "scd": merchant_id,
            "pid": pid,
            "rid": verification_code,
        }
        url = self.get_base_url(sandbox_mode)

        if payment_lookup_url.startswith("/"):
            payment_lookup_url = payment_lookup_url[1:]
        url = f"{url}{payment_lookup_url}"
        response_json = {}
        response = requests.post(url, params=d, timeout=10)
        check_response(
            response,
            "esewa-payment-lookup",
            "Error encountered while verifying your payment.",
        )
        if response.status_code == 200:
            response_json["paymentComplete"] = True
        else:
            response_json["paymentExpired"] = True
        return response_json

    def get_payment_url_with_pidx(self, payment_method, pidx, *args, **kwargs):
        sandbox_mode = payment_method.sandbox_mode
        payment_initiate_url = self.config.get("payment-initiate")
        merchant_id = payment_method.config.get("merchant")
        url = self.get_base_url(sandbox_mode)
        amount = kwargs.get("amount")
        amount = amount / 100
        success_link = kwargs.get("success_url")
        fail_link = kwargs.get("failure_url")
        if payment_initiate_url.startswith("/"):
            payment_initiate_url = payment_initiate_url[1:]
        url = f"{url}{payment_initiate_url}"
        url += f"?amt={amount}&tAmt={amount}&pdc=0&psc=0&scd={merchant_id}&pid={pidx}&txAmt=0&su={success_link}&fu={fail_link}"
        return url
