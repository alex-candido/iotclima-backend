# django_app/modules/v1/places/serializers.py

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Place, PlaceType, Status

User = get_user_model()


class PlacesInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)
    
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    status = serializers.ChoiceField(choices=Status.choices, default=Status.ACTIVE)
    type = serializers.ChoiceField(choices=PlaceType.choices, default=PlaceType.OTHER)
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,              
        allow_null=True 
    )

    def validate(self, attrs):
        if (attrs.get('latitude') is None) != (attrs.get('longitude') is None):
            raise serializers.ValidationError("Both 'latitude' and 'longitude' must be provided, or neither.")
        return attrs

class PlacesOutputSerializer(GeoFeatureModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True, required=False)
    user_email = serializers.CharField(source='user.email', read_only=True, required=False)
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Place
        fields = (
            'id', 'uuid', 'name', 'description', 'address', 'city', 'state', 'country',
            'status_display',
            'type_display',   
            'user',
            'user_username', 'user_email', 
            'created_at', 'updated_at',
            'location', 
        )
        geo_field = 'location'