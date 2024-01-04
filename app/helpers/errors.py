from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import exception_handler

from helpers.exceptions import BaseException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, ValidationError):
        return Response(
            {"error": exc.detail, "status_code": exc.status_code},
            status=exc.status_code,
        )
    if isinstance(exc, BaseException):
        return Response(
            {"error": exc.message, "status_code": exc.status_code},
            status=exc.status_code,
        )
    # Now add the HTTP status code to the response.
    if response is not None:
        status_code = response.data.get("status_code")
        if status_code:
            response.data["status_code"] = int(status_code[0])
        else:
            response.data["status_code"] = response.status_code

    return response
