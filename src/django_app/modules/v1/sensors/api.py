# django_app/modules/v1/sensors/api.py

from typing import Type, Union, Any, List
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from django_app.container import core_container

from .serializers import SensorsInputSerializer, SensorsOutputSerializer
from .services import SensorsService


class SensorsViewSet(viewsets.ViewSet):
    service: SensorsService = core_container.sensors_container.service()

    @staticmethod
    def _validated_data(serializer_class: Type[Serializer], data: Union[dict, List[dict], Any], **kwargs) -> Any:
        serializer = serializer_class(data=data, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @staticmethod
    def _to_response(serializer_class: Type[Serializer], output: Union[dict, List[dict], Any], **kwargs) -> Union[dict, List[dict], Any]:
        serializer = serializer_class(output, **kwargs)
        return serializer.data

    # GET /sensors/
    def list(self, request):
        output = self.service.list()
        data = self._to_response(SensorsOutputSerializer, output, many=True)
        return Response(data)

    # POST /sensors/
    def create(self, request):
        input_data = self._validated_data(SensorsInputSerializer, data=request.data)
        output = self.service.create(input_data)
        data = self._to_response(SensorsOutputSerializer, output)
        return Response(data, status=status.HTTP_201_CREATED)

    # GET /sensors/{pk}/
    def retrieve(self, request, pk=None):
        output = self.service.retrieve(pk)
        data = self._to_response(SensorsOutputSerializer, output)
        return Response(data)

    # PUT /sensors/{pk}/
    def update(self, request, pk=None):
        input_data = self._validated_data(SensorsInputSerializer, data=request.data)
        output = self.service.update(pk, input_data)
        data = self._to_response(SensorsOutputSerializer, output)
        return Response(data)

    # PATCH /sensors/{pk}/
    def partial_update(self, request, pk=None):
        instance = self.service.get_instance(pk)
        input_data = self._validated_data(SensorsInputSerializer, data=request.data, instance=instance, partial=True)
        output = self.service.update(pk, input_data)
        data = self._to_response(SensorsOutputSerializer, output)
        return Response(data)

    # DELETE /sensors/{pk}/
    def destroy(self, request, pk=None):
        self.service.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
