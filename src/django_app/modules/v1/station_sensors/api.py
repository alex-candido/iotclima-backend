# django_app/modules/v1/station_sensors/api.py

from typing import Any, List, Type, Union

from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from django_app.container import core_container

from .serializers import (StationSensorInputSerializer,
                          StationSensorOutputSerializer)
from .services import StationSensorService


class StandardResultsPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size' 
    max_page_size = 100
    
    def get_paginated_response(self, data, total_count=None):
        response_data = {
            'total_count': total_count if total_count is not None else 0,
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        }
        return Response(response_data)

class StationSensorViewSet(viewsets.ViewSet):
    service: StationSensorService = core_container.station_sensors_container.service()
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

    # GET /station_sensors/
    def list(self, request):
        filtered_queryset, total_count = self.service.list(query_params=request.query_params)
        
        if request.query_params.get('count_only') == 'true':
            count = filtered_queryset.count()
            return Response({'count': count}, status=status.HTTP_200_OK)
        
        page = self.pagination_class.paginate_queryset(filtered_queryset, request, view=self)
        serializer = StationSensorOutputSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data, total_count=total_count)

    # POST /station_sensors/
    def create(self, request):
        input_data = self._validated_data(StationSensorInputSerializer, data=request.data)
        output = self.service.create(input_data)
        data = self._to_response(StationSensorOutputSerializer, output)
        return Response(data, status=status.HTTP_201_CREATED)

    # GET /station_sensors/{pk}/
    def retrieve(self, request, pk=None):
        output = self.service.retrieve(pk)
        data = self._to_response(StationSensorOutputSerializer, output)
        return Response(data)

    # PUT /station_sensors/{pk}/
    def update(self, request, pk=None):
        instance = self.service.get_instance(pk)
        input_data = self._validated_data(StationSensorInputSerializer, data=request.data, instance=instance, partial=False)
        output = self.service.update(pk, input_data)
        data = self._to_response(StationSensorOutputSerializer, output)
        return Response(data)

    # PATCH /station_sensors/{pk}/
    def partial_update(self, request, pk=None):
        instance = self.service.get_instance(pk)
        input_data = self._validated_data(StationSensorInputSerializer, data=request.data, instance=instance, partial=True)
        output = self.service.update(pk, input_data)
        data = self._to_response(StationSensorOutputSerializer, output)
        return Response(data)

    # DELETE /station_sensors/{pk}/
    def destroy(self, request, pk=None):
        self.service.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
