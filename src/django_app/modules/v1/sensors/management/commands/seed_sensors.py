# django_app/modules/v1/sensors/management/commands/seed_sensors.py

import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.utils import IntegrityError
from faker import Faker

from django_app.modules.v1.sensors.models import (Sensor, SensorStatus,
                                                  SensorType, UnitType)

User = get_user_model()
fake = Faker('en_US')

SENSOR_TYPE_PROPERTIES = {
    SensorType.TEMPERATURE: {'unit_enum': UnitType.CELSIUS, 'min_value': -40.0, 'max_value': 60.0, 'model_suffix': 'THERM'},
    SensorType.HUMIDITY:    {'unit_enum': UnitType.PERCENT, 'min_value': 0.0,   'max_value': 100.0, 'model_suffix': 'HYGRO'},
    SensorType.WIND:        {'unit_enum': UnitType.METERS_PER_SECOND, 'min_value': 0.0, 'max_value': 50.0, 'model_suffix': 'ANEMO'},
    SensorType.PRESSURE:    {'unit_enum': UnitType.HECTOPASCAL, 'min_value': 900.0, 'max_value': 1100.0, 'model_suffix': 'BARO'},
    SensorType.RAINFALL:    {'unit_enum': UnitType.MILLIMETERS, 'min_value': 0.0,   'max_value': 500.0, 'model_suffix': 'PLUVIO'},
    SensorType.OTHER:       {'unit_enum': UnitType.OTHER, 'min_value': -1000.0, 'max_value': 1000.0, 'model_suffix': 'MISC'},
}


class Command(BaseCommand):
    help = 'Seeds the database with a small set of Sensor data (one for each type).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            default='development',
            help='Seeding mode: development or production (default: development)',
        )

    def _seed_development_mode(self):
        self.stdout.write("--- Seeding Sensors in Development Mode ---")

        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                raise CommandError("Admin user not found. Please run 'python manage.py seed_users' first.")
        except Exception as e:
            raise CommandError(f"Error fetching superuser: {e}")

        total_sensors_created = 0
        
        sensor_types_to_create = list(SensorType.values)

        with transaction.atomic():
            for sensor_type_value in sensor_types_to_create:
                if sensor_type_value == SensorType.OTHER:
                    self.stdout.write(f"Skipping creation of SensorType.OTHER.")
                    continue

                type_properties = SENSOR_TYPE_PROPERTIES.get(sensor_type_value, SENSOR_TYPE_PROPERTIES[SensorType.OTHER])
                
                sensor_type_display = SensorType(sensor_type_value).label
                sensor_model_name = f"{type_properties['model_suffix']}_{sensor_type_display.upper().replace(' ', '_')}_{fake.unique.random_int(100, 999)}"

                sensor_data = {
                    'type': sensor_type_value,
                    'model': sensor_model_name,
                    'unit': type_properties['unit_enum'],
                    'min_value': type_properties['min_value'],
                    'max_value': type_properties['max_value'],
                    'status': random.choice(list(SensorStatus.values)),
                    'user': admin_user,
                }

                try:
                    existing_sensor = Sensor.objects.filter(
                        model=sensor_data['model'],
                        type=sensor_data['type'],
                        unit=sensor_data['unit']
                    ).first()

                    if existing_sensor:
                        self.stdout.write(f"Sensor '{existing_sensor.model}' ({existing_sensor.get_type_display()} - {existing_sensor.get_unit_display()}) already exists. Skipping creation.") # type: ignore
                        continue

                    sensor = Sensor(**sensor_data)
                    sensor.save()

                    self.stdout.write(f"Created sensor: '{sensor.model}' (Type: {sensor.get_type_display()} - Unit: {sensor.get_unit_display()})") # type: ignore
                    total_sensors_created += 1

                except IntegrityError as e:
                    self.stdout.write(self.style.WARNING(f"Sensor '{sensor_data['model']}' has an integrity error. Skipping. Error: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error creating sensor '{sensor_data['model']}': {e}"))

        self.stdout.write(self.style.SUCCESS(f"Development mode seeding completed. Total sensors created: {total_sensors_created}"))

    def _seed_production_mode(self):
        self.stdout.write("--- Seeding Sensors in Production Mode ---")
        self.stdout.write(self.style.WARNING("Production mode for sensors seeding is not implemented. Please add specific logic if needed."))

    def handle(self, *args, **options):
        mode = options['mode']

        self.stdout.write(self.style.SUCCESS(f"--- Starting Sensor Seeding in '{mode}' Mode ---"))

        if mode == 'development':
            self._seed_development_mode()
        elif mode == 'production':
            self._seed_production_mode()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}. Use 'development' or 'production'."))

        self.stdout.write(self.style.SUCCESS("Sensor seeding process finished."))