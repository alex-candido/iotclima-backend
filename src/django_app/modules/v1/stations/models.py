# django_app/modules/v1/stations/models.py

import uuid

from django.conf import settings
from django.db import models

from django_app.modules.v1.places.models import Place


class StationStatus(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 0, 'Inactive'
    ONLINE = 2, 'Online'
    OFFLINE = 3, 'Offline'
    MAINTENANCE = 4, 'Maintenance'


class Station(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    model = models.CharField(max_length=255)
    firmware = models.CharField(max_length=255, blank=True, null=True)
    
    installed_at = models.DateTimeField(null=True, blank=True)
    last_maintenance_at = models.DateTimeField(null=True, blank=True)
    next_maintenance_at = models.DateTimeField(null=True, blank=True)
    
    battery_level = models.IntegerField(null=True, blank=True)
    signal_strength = models.IntegerField(null=True, blank=True)
    
    status = models.IntegerField(choices=StationStatus.choices, default=StationStatus.ACTIVE)
    
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='stations'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='stations_managed'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.place.name}"

