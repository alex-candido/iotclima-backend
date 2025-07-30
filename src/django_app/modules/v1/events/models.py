# django_app/modules/v1/events/models.py

import uuid

from django.conf import settings
from django.db import models

from django_app.modules.v1.sensors.models import Sensor
from django_app.modules.v1.station_sensors.models import StationSensor


class EventType(models.IntegerChoices):
    ALERT = 1, 'Alert'
    WARNING = 2, 'Warning'
    INFO = 3, 'Info'
    ERROR = 4, 'Error'

class EventCategory(models.IntegerChoices):
    WEATHER = 1, 'Weather'
    SENSOR = 2, 'Sensor'
    SYSTEM = 3, 'System'
    MAINTENANCE = 4, 'Maintenance'

class EventSeverity(models.IntegerChoices):
    LOW = 1, 'Low'
    MEDIUM = 2, 'Medium'
    HIGH = 3, 'High'
    CRITICAL = 4, 'Critical'

class EventStatus(models.IntegerChoices):
    OPEN = 1, 'Open'
    ACKNOWLEDGED = 2, 'Acknowledged'
    RESOLVED = 3, 'Resolved'


class Event(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    description = models.TextField()
    occurred_at = models.DateTimeField()
    resolved_at = models.DateTimeField(null=True, blank=True)

    type = models.IntegerField(
        choices=EventType.choices
    )
    category = models.IntegerField(
        choices=EventCategory.choices
    )
    severity = models.IntegerField(
        choices=EventSeverity.choices
    )
    status = models.IntegerField(
        choices=EventStatus.choices,
        default=EventStatus.OPEN
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, 
        null=True,
        related_name='events_created'
    )

    station_sensor = models.ForeignKey(
        StationSensor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-occurred_at'] 

    def __str__(self):
        station_name = self.station_sensor.station.name if self.station_sensor else "Unknown Station" # type: ignore
        return f"[{self.get_type_display()}] {self.title} (Station: {station_name})"# type: ignore