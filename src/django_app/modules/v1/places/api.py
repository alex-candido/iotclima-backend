# django_app/modules/v1/places/api.py

from typing import Any, List, Type, Union

from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from django_app.container import core_container

from .serializers import PlacesInputSerializer, PlacesOutputSerializer
from .services import PlacesService


# Define a custom Pagination class
class StandardResultsPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size' 
    max_page_size = 100 


class PlacesViewSet(viewsets.ViewSet):
    service: PlacesService = core_container.places_container.service()
    pagination_class = StandardResultsPagination() 

    @staticmethod
    def _validated_data(serializer_class: Type[Serializer], data: Union[dict, List[dict], Any], **kwargs) -> Any:
        serializer = serializer_class(data=data, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @staticmethod
    def _to_response(serializer_class: Type[Serializer], output: Union[dict, List[dict], Any], **kwargs) -> Union[dict, List[dict], Any]:
        serializer = serializer_class(output, **kwargs)
        return serializer.data

    # GET /places/
    def list(self, request):
        filtered_queryset = self.service.list(query_params=request.query_params)
        page = self.pagination_class.paginate_queryset(filtered_queryset, request, view=self)
        serializer = PlacesOutputSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

    # POST /places/
    def create(self, request):
        input_data = self._validated_data(PlacesInputSerializer, data=request.data)
        output = self.service.create(input_data)
        data = self._to_response(PlacesOutputSerializer, output)
        return Response(data, status=status.HTTP_201_CREATED)

    # GET /places/{pk}/
    def retrieve(self, request, pk=None):
        output = self.service.retrieve(pk)
        data = self._to_response(PlacesOutputSerializer, output)
        return Response(data)

    # PUT /places/{pk}/
    def update(self, request, pk=None):
        input_data = self._validated_data(PlacesInputSerializer, data=request.data)
        output = self.service.update(pk, input_data)
        data = self._to_response(PlacesOutputSerializer, output)
        return Response(data)

    # PATCH /places/{pk}/
    def partial_update(self, request, pk=None):
        instance = self.service.get_instance(pk)
        input_data = self._validated_data(PlacesInputSerializer, data=request.data, instance=instance, partial=True)
        output = self.service.update(pk, input_data)
        data = self._to_response(PlacesOutputSerializer, output)
        return Response(data)

    # DELETE /places/{pk}/
    def destroy(self, request, pk=None):
        self.service.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
