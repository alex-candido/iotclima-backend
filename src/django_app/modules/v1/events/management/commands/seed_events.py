# django_app/modules/v1/events/management/commands/seed_events.py

import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from django_app.modules.v1.events.models import (Event, EventCategory,
                                                 EventSeverity, EventStatus,
                                                 EventType)
from django_app.modules.v1.records.models import Record
# NOVO: Não precisa importar Station aqui, pois o Record já tem, e Event vai via StationSensor
# from django_app.modules.v1.stations.models import Station
from django_app.modules.v1.sensors.models import Sensor, SensorType
from django_app.modules.v1.station_sensors.models import StationSensor

User = get_user_model()


class Command(BaseCommand):
    help = 'Generates Events based on existing Record data and predefined rules.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            default='development',
            help='Seeding mode: development or production (default: development)',
        )

    def _seed_development_mode(self):
        self.stdout.write("--- Generating Events in Development Mode ---")

        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                raise CommandError("Admin user not found. Please run 'python manage.py seed_users' first.")
        except Exception as e:
            raise CommandError(f"Error fetching admin user: {e}")

        all_records = Record.objects.select_related('station', 'station__place').order_by('station', 'recorded_at')
        if not all_records.exists():
            raise CommandError("No records found. Please run 'python manage.py seed_records' first.")

        all_active_station_sensors = StationSensor.objects.select_related('sensor', 'station').filter(is_active=True).all()
        all_station_sensors_by_type = {
            st_value: [
                link for link in all_active_station_sensors if link.sensor.type == st_value
            ]
            for st_value in list(SensorType.values) if st_value != SensorType.OTHER
        }
        
        for sensor_type_value in [st_val for st_val in SensorType.values if st_val != SensorType.OTHER]:
            if not all_station_sensors_by_type.get(sensor_type_value):
                self.stdout.write(self.style.WARNING(f"Warning: No active StationSensor link found for SensorType '{SensorType(sensor_type_value).label}'. Events for this type might be skipped."))


        total_events_generated = 0
        
        with transaction.atomic():
            for record in all_records:
                events_for_this_record = [] 
                
                active_links_for_current_station = list(
                    record.station.station_sensor_links.filter(is_active=True) # type: ignore
                )
                
                active_links_by_sensor_type_for_station = {}
                for link in active_links_for_current_station:
                    if link.sensor.type not in active_links_by_sensor_type_for_station:
                        active_links_by_sensor_type_for_station[link.sensor.type] = []
                    active_links_by_sensor_type_for_station[link.sensor.type].append(link)

                # --- Regras de Eventos ---

                # Regra 1: Temperatura Moderadamente Alta
                if record.temperature is not None and record.temperature > 29.0:
                    sensor_type_for_rule = SensorType.TEMPERATURE
                    link_pool = active_links_by_sensor_type_for_station.get(sensor_type_for_rule)
                    if link_pool:
                        link_for_event = random.choice(link_pool)
                        events_for_this_record.append({
                            'title': "Moderate Temperature Alert",
                            'description': f"Temperature exceeded 29°C: {record.temperature}°C",
                            'type': EventType.WARNING,
                            'category': EventCategory.WEATHER,
                            'severity': EventSeverity.MEDIUM,
                            'status': EventStatus.OPEN,
                            'user': admin_user,
                            # REMOVIDO: 'station': record.station,
                            'station_sensor': link_for_event, # Associa ao StationSensor
                            'occurred_at': record.recorded_at,
                        })

                # Regra 2: Chuva Detectada
                if record.rainfall is not None and record.rainfall > 0.0:
                    sensor_type_for_rule = SensorType.RAINFALL
                    link_pool = active_links_by_sensor_type_for_station.get(sensor_type_for_rule)
                    if link_pool:
                        link_for_event = random.choice(link_pool)
                        events_for_this_record.append({
                            'title': "Rainfall Detected",
                            'description': f"Rainfall detected: {record.rainfall}mm",
                            'type': EventType.INFO,
                            'category': EventCategory.WEATHER,
                            'severity': EventSeverity.LOW,
                            'status': EventStatus.OPEN,
                            'user': admin_user,
                            # REMOVIDO: 'station': record.station,
                            'station_sensor': link_for_event,
                            'occurred_at': record.recorded_at,
                        })
                
                # Regra 3: Umidade Moderadamente Baixa
                if record.humidity is not None and record.humidity < 60.0:
                    sensor_type_for_rule = SensorType.HUMIDITY
                    link_pool = active_links_by_sensor_type_for_station.get(sensor_type_for_rule)
                    if link_pool:
                        link_for_event = random.choice(link_pool)
                        events_for_this_record.append({
                            'title': "Moderate Low Humidity",
                            'description': f"Humidity below 60%: {record.humidity}%",
                            'type': EventType.INFO,
                            'category': EventCategory.WEATHER,
                            'severity': EventSeverity.LOW,
                            'status': EventStatus.OPEN,
                            'user': admin_user,
                            # REMOVIDO: 'station': record.station,
                            'station_sensor': link_for_event,
                            'occurred_at': record.recorded_at,
                        })

                # Regra 4: Vento Moderadamente Forte
                if record.wind_speed is not None and record.wind_speed > 5.0:
                    sensor_type_for_rule = SensorType.WIND
                    link_pool = active_links_by_sensor_type_for_station.get(sensor_type_for_rule)
                    if link_pool:
                        link_for_event = random.choice(link_pool)
                        events_for_this_record.append({
                            'title': "Moderate Wind Speed",
                            'description': f"Wind speed exceeded 5 m/s: {record.wind_speed} m/s",
                            'type': EventType.INFO,
                            'category': EventCategory.WEATHER,
                            'severity': EventSeverity.LOW,
                            'status': EventStatus.OPEN,
                            'user': admin_user,
                            # REMOVIDO: 'station': record.station,
                            'station_sensor': link_for_event,
                            'occurred_at': record.recorded_at,
                        })

                for event_data in events_for_this_record:
                    try:
                        Event.objects.create(**event_data)
                        self.stdout.write(f"Generated Event: '{event_data['title']}' for Record {record.id} (Station '{record.station.name}')") # type: ignore
                        total_events_generated += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error creating event for Record (ID {record.id}): {e}")) # type: ignore
            
        self.stdout.write(self.style.SUCCESS(f"Development mode event generation completed. Total events created: {total_events_generated}"))

    def _seed_production_mode(self):
        self.stdout.write("--- Generating Events in Production Mode ---")
        self.stdout.write(self.style.WARNING("Production mode for events generation is not implemented. Please add specific logic if needed."))

    def handle(self, *args, **options):
        mode = options['mode']

        self.stdout.write(self.style.SUCCESS(f"--- Starting Event Seeding in '{mode}' Mode ---"))

        if mode == 'development':
            self._seed_development_mode()
        elif mode == 'production':
            self._seed_production_mode()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}. Use 'development' or 'production'."))

        self.stdout.write(self.style.SUCCESS("Event seeding process finished."))