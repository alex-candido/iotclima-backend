# django_app/modules/v1/Stations/repositories.py

from .models import Station, StationStatus


class StationsRepository:

    def list(self):
        return Station.objects.all()

    def create(self, validated_data):
        return Station.objects.create(**validated_data)

    def get(self, pk):
        return Station.objects.get(pk=pk)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.status = StationStatus.INACTIVE 
        instance.save()
