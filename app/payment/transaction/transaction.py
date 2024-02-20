from payment.transaction import Transaction
from website.models import Config
from helpers.mixins.helper import generate_random_string
from helpers.exceptions import InvalidOperationException
import logging
from django.utils import timezone
from datetime import timedelta
import requests
from payment.models import PaymentMethod
from helpers.mixins.helper import get_hashed_signed
import json
from payment.constant import PaymentStatus


class Esewa(Transaction):
    def get_config(self):
        try:
            config = PaymentMethod.objects.get(name="Esewa").config
            paymenty_initiate = config.get("payment-initiate")
            live_verify_url = config.get("live-verify-url")
            sandbox_verify_url = config.get("sandbox-verify-url")
            verify_payment = config.get("verify-payment")
            sandbox_endpoint = config.get("sandbox-endpoint")
            live_endpoint = config.get("live-endpoint")
            if (
                not paymenty_initiate
                or not verify_payment
                or not sandbox_endpoint
                or not live_endpoint
                or not live_verify_url
                or not sandbox_verify_url
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

    def payment_verify(self, payment_method, **kwargs):
        sandbox_mode = payment_method.enable_sandbox
        payment_lookup_url = self.config.get("verify-payment")
        product_code = payment_method.config.get("product_code")
        transaction_uuid = kwargs.get("transaction_uuid")
        amount = kwargs.get("amount")
        if sandbox_mode:
            url = self.config.get("sandbox-verify-url")
        else:
            url = self.config.get("live-verify-url")
        params = {
            "product_code": product_code,
            "total_amount": amount / 100,
            "transaction_uuid": transaction_uuid,
        }
        response_json = {}
        url = (
            url
            + payment_lookup_url
            + f"?product_code={product_code}&total_amount={amount/100}&transaction_uuid={transaction_uuid}"
        )
        response = requests.get(url)
        response_json = response.json()
        if response_json["status"] == "COMPLETE":
            return PaymentStatus.COMPLETE
        elif response_json["status"] == "PENDING":
            return PaymentStatus.PENDING
        elif response_json["status"] == "CANCLED":
            return PaymentStatus.CANCEL
        return PaymentStatus.EXPIRED

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

    def payment_initiate(self, payment_method, *args, **kwargs):
        secret = "8gBm/:&EnhH.1/q"
        transaction_uuid = kwargs.get("transaction_uuid")
        amount = kwargs.get("amount")
        product_code = payment_method.config.get("product_code")
        fields = {
            "total_amount": amount,
            "transaction_uuid": transaction_uuid,
            "product_code": product_code,
        }
        hashed_signed = get_hashed_signed(secret=secret, **fields)
        sandbox_mode = payment_method.enable_sandbox
        url = self.get_base_url(sandbox_mode)
        payment_initiate = payment_method.config.get("payment-initiate")
        product_code = payment_method.config.get("product_code")
        form_data = {
            "amount": amount,
            "product_delivery_charge": "0",
            "product_service_charge": "0",
            "product_code": product_code,
            "signature": hashed_signed,
            "signed_field_names": f"total_amount,transaction_uuid,product_code",
            "success_url": kwargs.get("success_url"),
            "failure_url": kwargs.get("failure_url"),
            "tax_amount": "0",
            "total_amount": amount,
            "transaction_uuid": transaction_uuid,
        }
        response = requests.post(url + payment_initiate, data=form_data)
        if response.status_code == 200:
            return response.url
        raise BaseException("Error while initiating payment")
