import uuid
import string
import random

import hmac
import hashlib
import base64


def generate_random_string(N=8):
    res = "".join(random.choices(string.ascii_uppercase + string.digits, k=N))
    return str(res)


class GenerateIID:
    def generate_iid(self, key="iid"):
        iid = uuid.uuid1()
        iid = key + "_" + str(iid).replace("-", "")
        return iid


def get_permission_request(request, user):
    pass


def get_hashed_signed(secret: str, **kwargs):
    total_amount = kwargs.get("total_amount")
    transaction_uuid = kwargs.get("transaction_uuid")
    product_code = kwargs.get("product_code")
    signed_fields = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    secret = secret
    hash = hmac.new(
        secret.encode(), signed_fields.encode(), digestmod=hashlib.sha256
    ).digest()
    hash_in_base64 = base64.b64encode(hash).decode()
    return hash_in_base64
