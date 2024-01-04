from rest_framework import status
from rest_framework.exceptions import APIException


class BaseException(APIException):
    """
    Base exception for every Amphi exception.
    """

    # message: display message for each exception
    # error_key: error key of each exception: defaults to error

    def __init__(
        self, message, error_key="error", status_code=status.HTTP_400_BAD_REQUEST
    ):
        super(BaseException, self).__init__(message, error_key)
        self.message = message
        self.error_key = error_key
        self.status_code = status_code


class SerializerNotFoundException(BaseException):
    def __init__(
        self,
        message="Serializer not found",
        error_key="error",
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
    ):
        super().__init__(message, error_key, status_code)
        self.message = {"message": [message]}
        self.error_key = error_key
        self.status_code = status_code


class NotFoundException(BaseException):
    def __init__(
        self,
        message="data not found",
        error_key="error",
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
    ):
        super().__init__(message, error_key, status_code)
        self.message = {"message": [message]}
        self.error_key = error_key
        self.status_code = status_code


class RequiredException(BaseException):
    def __init__(
        self,
        message="Param not provided",
        error_key="error",
        status_code=status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message, error_key, status_code)
        self.message = {"message": message}
        self.error_key = error_key
        self.status_code = status_code
