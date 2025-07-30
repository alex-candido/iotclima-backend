# django_app/modules/v1/places/models.py

import uuid

from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.db import models


class Status(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 0, 'Inactive'

class PlaceType(models.IntegerChoices):
    FARM = 1, 'Farm'
    CAMPUS = 2, 'Campus'
    CITY = 3, 'City'
    RESERVE = 4, 'Reserve'
    OTHER = 5, 'Other'

class Place(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    location = gis_models.PointField(srid=4326, geography=True)
    
    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVE)
    type = models.IntegerField(choices=PlaceType.choices, default=PlaceType.OTHER)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, 
        related_name='places'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def set_location(self, lat: float, lng: float):
        self.location = Point(lng, lat, srid=4326)

