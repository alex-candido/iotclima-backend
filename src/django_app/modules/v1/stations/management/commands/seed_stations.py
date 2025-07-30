# django_app/modules/v1/stations/management/commands/seed_stations.py

import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from faker import Faker

# Import models and Enums
from django_app.modules.v1.places.models import Place
from django_app.modules.v1.stations.models import Station, StationStatus

User = get_user_model()
fake = Faker('en_US')

class Command(BaseCommand):
    help = 'Seeds the database with Station data, creating stations for each existing Place.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            default='development',
            help='Seeding mode: development or production (default: development)',
        )
        parser.add_argument(
            '--stations_per_place',
            type=int,
            default=1,
            help='Number of stations to create per place in development mode.',
        )

    def _seed_development_mode(self, stations_per_place):
        self.stdout.write("--- Seeding Stations in Development Mode ---")

        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                raise CommandError("Admin user not found. Please run 'python manage.py seed_users' first.")
        except Exception as e:
            raise CommandError(f"Error fetching superuser: {e}")

        all_places = list(Place.objects.all())
        if not all_places:
            raise CommandError("No places found. Please run 'python manage.py seed_places' or 'seed_places_from_csv' first to create places.")

        total_stations_created = 0
        with transaction.atomic():
            for place in all_places:
                for i in range(stations_per_place):
                    base_name_for_station = place.name.split('_')[0] if '_' in place.name else place.name
                    station_name = f"{base_name_for_station}_STATION_{i+1:03d}"

                    # Gerar datetimes como "naive" e depois torná-los "aware"
                    installed_at_naive = fake.date_time_between(start_date='-2y', end_date='now')
                    last_maintenance_at_naive = fake.date_time_between(start_date='-1y', end_date='now')
                    next_maintenance_at_naive = fake.date_time_between(start_date='now', end_date='+1y')

                    # Converte para datetime "aware" usando o fuso horário atual do Django
                    installed_at_aware = timezone.make_aware(installed_at_naive)
                    last_maintenance_at_aware = timezone.make_aware(last_maintenance_at_naive)
                    next_maintenance_at_aware = timezone.make_aware(next_maintenance_at_naive)

                    station_data = {
                        'name': station_name,
                        'description': f"Station for {place.name} in {place.city}, {place.state}.",
                        'model': fake.word().upper() + "XYZ-" + str(fake.random_int(100, 999)),
                        'firmware': f"v{fake.random_int(1, 9)}.{fake.random_int(0, 9)}",
                        'installed_at': installed_at_aware,
                        'last_maintenance_at': last_maintenance_at_aware,
                        'next_maintenance_at': next_maintenance_at_aware,
                        'battery_level': random.randint(20, 100),
                        'signal_strength': random.randint(-90, -30), 
                        'status': random.choice(list(StationStatus.values)), 
                        'place': place, 
                        'user': admin_user 
                    }

                    try:
                        existing_station = Station.objects.filter(name=station_name, place=place).first()
                        if existing_station:
                            self.stdout.write(f"Station '{station_name}' for Place '{place.name}' already exists. Skipping creation.")
                            continue

                        station = Station(**station_data)
                        station.save()

                        self.stdout.write(f"Created station: '{station.name}' for Place: '{place.name}'")
                        total_stations_created += 1

                    except IntegrityError as e:
                        self.stdout.write(self.style.WARNING(f"Station '{station_name}' has an integrity error for Place '{place.name}'. Skipping. Error: {e}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error creating station '{station_name}' for Place '{place.name}': {e}"))

        self.stdout.write(self.style.SUCCESS(f"Development mode seeding completed. Total stations created: {total_stations_created}"))

    def _seed_production_mode(self):
        self.stdout.write("--- Seeding Stations in Production Mode ---")
        self.stdout.write(self.style.WARNING("Production mode for stations seeding is not implemented. Please add specific logic if needed."))

    def handle(self, *args, **options):
        mode = options['mode']
        stations_per_place = options['stations_per_place']

        self.stdout.write(self.style.SUCCESS(f"Starting station seeding in '{mode}' mode"))

        if mode == 'development':
            self._seed_development_mode(stations_per_place)
        elif mode == 'production':
            self._seed_production_mode()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}. Use 'development' or 'production'."))

        self.stdout.write(self.style.SUCCESS("Station seeding process finished."))