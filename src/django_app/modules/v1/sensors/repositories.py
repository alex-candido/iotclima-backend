# django_app/modules/v1/sensors/repositories.py

from .models import Sensors


class SensorsRepository:

    def list(self):
        return Sensors.objects.all()

    def create(self, validated_data):
        return Sensors.objects.create(**validated_data)

    def get(self, pk):
        return Sensors.objects.get(pk=pk)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
