# django_app/modules/v1/records/repositories.py

from .models import Record, Status


class RecordsRepository:
    def list(self):
        return Record.objects.all()

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def get(self, pk):
        return Record.objects.get(pk=pk)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.status = Status.INACTIVE
        instance.save()