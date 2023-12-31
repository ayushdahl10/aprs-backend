from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet

from helpers.exceptions import (
    SerializerNotFoundException,
    NotFoundException,
    RequiredException,
)
from helpers.mixins.api_mixins import APIMixin
from helpers.pagination import CustomPagination


# readonly viewset for reading methods
class ReadOnlyViewSet(APIMixin, ReadOnlyModelViewSet):
    lookup_field = "iid"
    list_serializer = None
    detail_serializer = None
    pagination_class = CustomPagination
    required_param: list = []

    def _get_default_serializer_class(self):
        if self.serializer_class:
            return self.serializer_class
        raise SerializerNotFoundException()

    def get_serializer_class(self):
        if self.action.lower() == "list":
            if not self.list_serializer:
                return self._get_default_serializer_class()
            return self.list_serializer
        if self.action.lower() == "retrieve":
            if not self.detail_serializer:
                return self._get_default_serializer_class()
            return self.detail_serializer
        return self.get_serializer

    def list(self, request, *args, **kwargs):
        if len(self.required_param) > 0:
            self.validate_required_params()
        queryset = kwargs.get("queryset", None)
        querysets = self.filter_queryset(
            queryset if queryset is not None else self.get_queryset()
        )
        if self.is_paginated:
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(
                querysets, request, view=self
            )
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(
                paginated_queryset, many=True, context={"request": request}
            )
            page_data, record_data = paginator.get_paginated_response(serializer.data)
            return self.on_api_success_pagination(
                page_data=page_data,
                records_data=record_data,
                status=status.HTTP_200_OK,
            )

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            querysets, many=True, context={"request": request}
        )
        return self.on_api_success_response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(iid=kwargs["iid"])
        except Exception:
            raise NotFoundException(
                message=f"Couldn't find object with iid {kwargs['iid']}.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            instance,
            context={"request": self.request},
        )
        return self.on_api_success_response(serializer.data, status=status.HTTP_200_OK)

    def validate_required_params(self):
        error_message: list = []
        for param in self.required_param:
            if self.request.query_params.get(param, None) is None:
                error_message.append(f"{param} is required in parameter")
        if len(error_message) > 0:
            raise RequiredException(message=error_message)
