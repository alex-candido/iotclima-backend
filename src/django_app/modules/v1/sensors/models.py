# django_app/modules/v1/sensors/models.py

from django.db import models
import uuid


class Sensors(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    uuid = models.UUIDField(default='uuid.uuid4')
    type = models.IntegerField;model=CharField(max_length=255)
    min_value = models.FloatField;max_value=FloatField;calibrated_at=DateTimeField(null=True)
    status = models.IntegerField;station=ForeignKey()
    user = models.ForeignKey()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
