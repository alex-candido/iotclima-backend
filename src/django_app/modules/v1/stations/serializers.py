# django_app/modules/v1/stations/serializers.py

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from django_app.modules.v1.places.models import Place

from .models import Station, StationStatus

User = get_user_model()


class StationsInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    model = serializers.CharField(max_length=255)
    firmware = serializers.CharField(max_length=255, allow_blank=True, required=False)

    installed_at = serializers.DateTimeField(allow_null=True, required=False)
    last_maintenance_at = serializers.DateTimeField(allow_null=True, required=False)
    next_maintenance_at = serializers.DateTimeField(allow_null=True, required=False)

    battery_level = serializers.IntegerField(allow_null=True, required=False)
    signal_strength = serializers.IntegerField(allow_null=True, required=False)

    status = serializers.ChoiceField(choices=StationStatus.choices, default=StationStatus.ACTIVE)

    place = serializers.PrimaryKeyRelatedField(
        queryset=Place.objects.all(),
        required=True
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )


class StationsOutputSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    place_name = serializers.CharField(source='place.name', read_only=True)
    place_city = serializers.CharField(source='place.city', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True, required=False, allow_null=True)
    user_email = serializers.CharField(source='user.email', read_only=True, required=False, allow_null=True)


    class Meta:
        model = Station
        fields = (
            'id', 'uuid', 'name', 'description', 'model', 'firmware',
            'installed_at', 'last_maintenance_at', 'next_maintenance_at',
            'battery_level', 'signal_strength',
            'status', 'status_display',
            'place', 'place_name', 'place_city',
            'user', 'user_username', 'user_email',
            'created_at', 'updated_at'
        )