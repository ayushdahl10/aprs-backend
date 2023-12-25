DEFAULT_KHALTI_CONFIG = {
    "prod_endpoint": "https://khalti.com/api/v2/",
    "sanbox_endpoint": "https://a.khalti.com/api/v2/",
    "initiate_payment": "epayment/initiate/",
    "payment_verification": "epayment/lookup/",
    "prod_sercret_key": "",
    "text_sercet_key": "",
}

DEFAULT_ESEWA_CONFIG = {
    "prod_endpoint": "",
    "sanbox_endpoint": "",
    "initiate_payment": "",
    "payment_verification": "",
}

DEFAULT_SCHEMA = [
    {
        "api_key": "prod_endpoint",
        "type": "url",
        "label": "Production Endpoint",
        "input_type": "text",
        "max_length": 256,
        "required": True,
    },
    {
        "api_key": "sandbox_endpoint",
        "type": "url",
        "label": "Sandbox Endpoint",
        "input_type": "text",
        "max_length": 256,
        "required": True,
    },
    {
        "api_key": "initiate_payment",
        "type": "url",
        "label": "Initiate Payment",
        "input_type": "text",
        "max_length": 256,
        "required": True,
    },
    {
        "api_key": "payment_verification",
        "type": "url",
        "label": "Payment Verification",
        "input_type": "text",
        "max_length": 256,
        "required": True,
    },
]


KHALTI = {
    "name": "Khalti",
    "config": DEFAULT_KHALTI_CONFIG,
    "schema": DEFAULT_SCHEMA,
    "is_active": True,
}

ESEWA = {
    "name": "Esewa",
    "config": DEFAULT_ESEWA_CONFIG,
    "schema": DEFAULT_SCHEMA,
    "is_active": True,
}

PAYMENT_CONFIG = {
    "khalti": KHALTI,
    "esewa": ESEWA,
}
