from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        return Response({"msg": "Cannot retrieve data", "status": 404})
    return exception_handler(exc, context)


class SuperBaseException(Exception):
    def custom_ex_handler(message):
        return Response()
