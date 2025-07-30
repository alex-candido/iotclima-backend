# django_app/modules/v1/logs/management/commands/seed_logs.py

import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from faker import Faker

from django_app.modules.v1.logs.models import Log, LogSeverity
from django_app.modules.v1.records.models import Record
from django_app.modules.v1.sensors.models import Sensor, SensorType
from django_app.modules.v1.station_sensors.models import StationSensor

User = get_user_model()
fake = Faker('en_US')


class Command(BaseCommand):
    help = 'Generates various types of Log entries based on system behavior scenarios.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            default='development',
            help='Seeding mode: development or production (default: development)',
        )
        parser.add_argument(
            '--log_ratio',
            type=float,
            default=0.5,
            help='Ratio (0.0-1.0) of records to simulate processing logs for.',
        )
        parser.add_argument(
            '--error_chance',
            type=float,
            default=0.05,
            help='Chance (0.0-1.0) of generating an ERROR log for a simulated record processing.',
        )
        parser.add_argument(
            '--warn_chance',
            type=float,
            default=0.15,
            help='Chance (0.0-1.0) of generating a WARN log for a simulated record processing.',
        )

    def _seed_development_mode(self, log_ratio, error_chance, warn_chance):
        self.stdout.write("--- Generating Log Entries in Development Mode ---")

        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                raise CommandError("Admin user not found. Please run 'python manage.py seed_users' first.")
        except Exception as e:
            raise CommandError(f"Error fetching admin user: {e}")

        all_records = Record.objects.select_related('station', 'station__place').order_by('station', 'recorded_at')
        if not all_records.exists():
            raise CommandError("No records found. Please run 'python manage.py seed_records' first.")

        all_station_sensor_links = list(StationSensor.objects.select_related('sensor', 'station').filter(is_active=True))
        
        def get_random_sensor_link_for_station(station_obj):
            links = list(station_obj.station_sensor_links.filter(is_active=True)) # type: ignore
            return random.choice(links) if links else None

        total_logs_created = 0
        with transaction.atomic():
            Log.objects.create(
                message="System initialized successfully. All services started.",
                level=LogSeverity.INFO,
                user=admin_user,
                station=None,
                metadata={"event_type": "system_startup"}
            )
            total_logs_created += 1
            self.stdout.write(f"Generated Log: System Startup (INFO)")

            for index, record in enumerate(all_records):
                if random.random() > log_ratio:
                    continue

                log_data = {
                    'message': "",
                    'level': LogSeverity.INFO,
                    'user': admin_user,
                    'station': record.station,
                    'metadata': {
                        "record_id": record.id, # type: ignore
                        "station_name": record.station.name,
                        "record_timestamp": record.recorded_at.isoformat()
                    }
                }

                log_type_roll = random.random()
                
                if log_type_roll < error_chance:
                    sensor_link = get_random_sensor_link_for_station(record.station)
                    error_type = random.choice(["DB_CONN_FAIL", "SENSOR_READ_ERROR", "DATA_PARSE_FAIL"])
                    
                    log_data['level'] = LogSeverity.ERROR
                    log_data['message'] = f"CRITICAL ERROR: Failed to process data for Record {record.id}." # type: ignore
                    
                    sensor_uuid_str = str(sensor_link.sensor.uuid) if sensor_link and sensor_link.sensor else None
                    log_data['metadata'].update({
                        "error_type": error_type,
                        "details": f"{error_type} occurred during processing.",
                        "sensor_uuid": sensor_uuid_str,
                        "sensor_model": sensor_link.sensor.model if sensor_link else None,
                        "position": sensor_link.position if sensor_link else None
                    })
                    self.stdout.write(self.style.ERROR(f"Generated Log: ERROR for Record {record.id} ({error_type})")) # type: ignore

                elif log_type_roll < warn_chance + error_chance:
                    sensor_link = get_random_sensor_link_for_station(record.station)
                    warning_type = random.choice(["API_TIMEOUT", "DATA_OUT_OF_RANGE", "LOW_SIGNAL"])

                    log_data['level'] = LogSeverity.WARN
                    log_data['message'] = f"WARNING: An issue occurred while processing Record {record.id}." # type: ignore
                    
                    sensor_uuid_str = str(sensor_link.sensor.uuid) if sensor_link and sensor_link.sensor else None
                    log_data['metadata'].update({
                        "warning_type": warning_type,
                        "details": f"{warning_type} detected for sensor data.",
                        "sensor_uuid": sensor_uuid_str,
                        "sensor_model": sensor_link.sensor.model if sensor_link else None,
                    })
                    self.stdout.write(self.style.WARNING(f"Generated Log: WARN for Record {record.id} ({warning_type})")) # type: ignore
                
                else:
                    log_data['level'] = LogSeverity.INFO
                    log_data['message'] = f"Record {record.id} processed successfully. Event rules evaluated." # type: ignore
                    log_data['metadata'].update({"status": "success"})
                    self.stdout.write(f"Generated Log: INFO for Record {record.id} (Success)") # type: ignore
                
                try:
                    Log.objects.create(**log_data)
                    total_logs_created += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Critical Error: Failed to save log for Record (ID {record.id}): {e}")) # type: ignore

        self.stdout.write(self.style.SUCCESS(f"Development mode log generation completed. Total logs created: {total_logs_created}"))

    def _seed_production_mode(self):
        self.stdout.write("--- Generating Log Entries in Production Mode ---")
        self.stdout.write(self.style.WARNING("Production mode for logs generation is not implemented. Please add specific logic if needed."))

    def handle(self, *args, **options):
        mode = options['mode']
        log_ratio = options['log_ratio']
        error_chance = options['error_chance']
        warn_chance = options['warn_chance']

        self.stdout.write(self.style.SUCCESS(f"--- Starting Log Seeding in '{mode}' Mode ---"))

        if mode == 'development':
            self._seed_development_mode(log_ratio, error_chance, warn_chance)
        elif mode == 'production':
            self._seed_production_mode()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}. Use 'development' or 'production'."))

        self.stdout.write(self.style.SUCCESS("Log seeding process finished."))