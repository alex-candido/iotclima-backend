# django_app/modules/v1/events/repositories.py

from .models import Event, EventStatus


class EventsRepository:
    def list(self):
        return Event.objects.all()

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def get(self, pk):
        return Event.objects.get(pk=pk)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.status = EventStatus.RESOLVED 
        instance.save()