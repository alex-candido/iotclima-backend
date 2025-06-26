# django_app/modules/v1/records/repositories.py

from django.core.exceptions import ObjectDoesNotExist
from .models import Record, Status
from typing import Any, Dict, Union, Type
from uuid import UUID

class RecordsRepository:
    def list(self):
        return Record.objects.all()

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def get(self, pk: Union[int, str, UUID]):
        try:
            uuid_obj = UUID(str(pk))
            return Record.objects.get(uuid=uuid_obj)
        except (ValueError, ObjectDoesNotExist):
            return Record.objects.get(id=pk)  

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.status = Status.INACTIVE
        instance.save()