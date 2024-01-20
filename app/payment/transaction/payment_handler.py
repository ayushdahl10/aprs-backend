from helpers.exceptions import NotFoundException
import logging
from payment.models import PaymentMethod
from payment.transaction import Esewa


def choose_payment_option_class(payment_name):
    if payment_name.lower() == "esewa":
        return Esewa
    raise NotFoundException("Invalid Payment Option")


def handle_payment_processing(payment_type, payment_method, *args, **kwargs):
    if not isinstance(payment_method, PaymentMethod):
        logging.error(msg=f"[{payment_type}] Invalid Payment Method instance.")
        raise NotFoundException("Error processing payment. Please try again later.")
    payment_name = payment_method.payment_name
    if payment_type == "initiate":
        return choose_payment_option_class(payment_name).payment_initiate(
            payment_method=payment_method, *args, **kwargs
        )
    elif payment_type == "get_url":
        return choose_payment_option_class(payment_name).get_payment_url_with_pidx(
            payment_method=payment_method, **kwargs
        )
    elif payment_type == "verify":
        return choose_payment_option_class(payment_name).payment_verify(
            payment_method=payment_method, *args, **kwargs
        )
    raise NotFoundException("Invalid Payment Type")
