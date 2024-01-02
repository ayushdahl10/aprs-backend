from django.db import transaction
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from helpers.exceptions import (
    SerializerNotFoundException,
    NotFoundException,
)
from helpers.mixins.api_mixins import APIMixin
from helpers.pagination import CustomPagination


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


"""base viewset for CRUD operations"""


class SuperViewset(
    APIMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    UpdateModelMixin,
    viewsets.GenericViewSet,
):
    lookup_field = "iid"
    list_serializer = None
    detail_serializer = None
    create_update_serializer = None
    pagination_class = CustomPagination
    force_delete: bool = False

    def _get_default_serializer_class(self):
        if self.serializer_class:
            return self.serializer_class
        raise SerializerNotFoundException()

    def get_serializer_class(self):
        if self.action.lower() == "list":
            if not self.list_serializer:
                return self._get_default_serializer_class()
            return self.list_serializer
        if self.action.lower() in ["create", "partial_update"]:
            if not self.create_update_serializer:
                return self._get_default_serializer_class()
            return self.create_update_serializer
        if self.action.lower() == "retrieve":
            if not self.detail_serializer:
                return self._get_default_serializer_class()
            return self.detail_serializer
        return self.get_serializer

    def list(self, request, *args, **kwargs):
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

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(iid=kwargs["iid"])
        except Exception:
            raise NotFoundException(
                message=f"Couldn't find object with iid {kwargs['iid']}.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            instance = serializer.save()
        return self.on_api_success_response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=self.request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.on_api_success_response(serializer.data, status=201)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.force_delete:
            instance.delete(force=True)
            return self.on_api_success_response("Deleted successfully", 200)
        instance.is_deleted = True
        instance.is_active = False
        instance.save()
        return self.on_api_success_response("Deleted successfully", 200)
