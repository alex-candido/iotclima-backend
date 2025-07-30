# django_app/modules/v1/places/migrations/0001_enable_postgis_extension.py

from django.contrib.postgres.operations import CreateExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'), 
    ]

    operations = [
        CreateExtension('postgis'),
        CreateExtension('postgis_topology'),
        CreateExtension('fuzzystrmatch'),
        CreateExtension('postgis_tiger_geocoder'),
    ]