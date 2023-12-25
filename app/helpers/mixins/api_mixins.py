from permissions.permission import WebPermission
from rest_framework.response import Response
from rest_framework.authentication import (
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from helpers.mixins.prerequest import RequestHandler


class APIMixin(RequestHandler):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [WebPermission]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def on_api_success_response(self, data, status, message="success", **kwargs):
        response = {
            "data": data,
            "status_code": status,
            "message": message,
        }
        return Response(response, status=status)

    def on_api_error_response(self, message, status):
        response = {
            "message": message,
            "status_code": status,
        }
        return Response(response, status)

    def on_api_success_pagination(
        self, page_data, records_data, status, message="success", **kwargs
    ):
        response = {
            "page_data": page_data,
            "records": records_data,
            "status_code": status,
            "message": message,
        }
        return Response(response, status=status)
