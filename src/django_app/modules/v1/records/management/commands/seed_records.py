import random
from datetime import datetime, timedelta
from datetime import timezone as dt_timezone

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from django_app.__shared.open_meteo_client import OpenMeteoClient
from django_app.modules.v1.records.models import Record, Status
from django_app.modules.v1.stations.models import Station


class Command(BaseCommand):
    help = 'Seeds the database with real meteorological records for each station by fetching hourly data from Open-Meteo.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            default='development',
            help='Seeding mode: development or production (default: development)',
        )
        parser.add_argument(
            '--days_of_data',
            type=int,
            default=1,
            help='Number of days of historical data to fetch for each station (e.g., 1 for 24 records).',
        )

    def _seed_development_mode(self, days_of_data):
        self.stdout.write("--- Seeding Meteorological Records in Development Mode ---")

        all_stations = Station.objects.select_related('place').all() 
        if not all_stations:
            raise CommandError("No stations found. Please ensure stations and places are seeded.")

        weather_client = OpenMeteoClient()

        total_records_created = 0
        with transaction.atomic():
            # Calculate the date range to fetch. 
            # Open-Meteo Archive API provides data for complete, archived days.
            # Fetching data for today or yesterday (if not fully closed in UTC) can result in None values.
            # So, we fetch data from at least two days ago.
            today_utc = datetime.now(dt_timezone.utc).date()
            end_date_for_api = today_utc - timedelta(days=2) # End date is 2 days ago
            start_date_for_api = end_date_for_api - timedelta(days=days_of_data - 1) # Start date based on days_of_data

            self.stdout.write(f"Fetching {days_of_data} day(s) of hourly data from {start_date_for_api} to {end_date_for_api} for each station.")

            for station in all_stations:
                if not station.place or not station.place.location:
                    self.stdout.write(self.style.WARNING(f"Station '{station.name}' has no linked place or location. Skipping."))
                    continue

                latitude = station.place.location.y 
                longitude = station.place.location.x 
                
                self.stdout.write(f"Fetching data for Station: '{station.name}' at ({latitude}, {longitude})...")

                hourly_weather_data_list = weather_client.get_hourly_historical_weather(
                    latitude, longitude, 
                    datetime.combine(start_date_for_api, datetime.min.time()).replace(tzinfo=dt_timezone.utc), 
                    datetime.combine(end_date_for_api, datetime.max.time()).replace(tzinfo=dt_timezone.utc) 
                )
                
                if hourly_weather_data_list:
                    records_for_station = 0
                    for weather_data in hourly_weather_data_list:
                        # Check for existing record to ensure idempotency
                        existing_record = Record.objects.filter(
                            station=station,
                            recorded_at=weather_data['recorded_at']
                        ).first()

                        if existing_record:
                            self.stdout.write(f"Record for '{station.name}' at {weather_data['recorded_at']} already exists. Skipping.")
                            continue

                        record_data = {
                            'station': station, 
                            'recorded_at': weather_data['recorded_at'],
                            'temperature': weather_data['temperature'],
                            'humidity': weather_data['humidity'],
                            'wind_speed': weather_data['wind_speed'],
                            'wind_direction': weather_data['wind_direction'],
                            'pressure': weather_data['pressure'],
                            'rainfall': weather_data['rainfall'],
                            'status': Status.ACTIVE 
                        }

                        try:
                            record = Record.objects.create(**record_data)
                            # Display temperature with unit if available
                            temp_output = f"{record.temperature}°C" if record.temperature is not None else "None°C"
                            self.stdout.write(f"Created record for '{station.name}' at {record.recorded_at} (Temp: {temp_output})")
                            total_records_created += 1
                            records_for_station += 1
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Error creating record for Station '{station.name}': {e}"))
                    self.stdout.write(f"Successfully created {records_for_station} records for Station '{station.name}'.")
                else:
                    self.stdout.write(self.style.WARNING(f"No weather data fetched for Station '{station.name}' in the specified period. Skipping record creation."))
                
            self.stdout.write(self.style.SUCCESS(f"Development mode seeding completed. Total records created: {total_records_created}"))

    def _seed_production_mode(self):
        self.stdout.write("--- Seeding Meteorological Records in Production Mode ---")
        self.stdout.write(self.style.WARNING("Production mode for records seeding is not implemented. Please add specific logic if needed."))

    def handle(self, *args, **options):
        mode = options['mode']
        days_of_data = options['days_of_data']

        self.stdout.write(self.style.SUCCESS(f"--- Starting Record Seeding in '{mode}' Mode ---"))

        if mode == 'development':
            self._seed_development_mode(days_of_data)
        elif mode == 'production':
            self._seed_production_mode()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}. Use 'development' or 'production'."))

        self.stdout.write(self.style.SUCCESS("Record seeding process finished."))