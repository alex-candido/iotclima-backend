# django_app/modules/v1/places/management/commands/seed_places_from_csv.py

import os

import pandas as pd
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.utils import IntegrityError

from django_app.modules.v1.places.models import Place, PlaceType, Status

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with place data loaded from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='../notebooks/data/places_data.csv',
            help='Path to CSV file relative to project root.',
        )
        parser.add_argument(
            '--mode',
            type=str,
            default='development',
            help='Seeding mode: development or production',
        )
        parser.add_argument(
            '--places_per_city',
            type=int,
            default=1,
            help='Number of places to create per city in development mode from CSV data.',
        )

    def _seed_development_mode(self, places_per_city, csv_path):
        self.stdout.write('--- Seeding Places in Development Mode ---')
        
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            raise CommandError("No superuser found. Please create one.")

        if not os.path.exists(csv_path):
            raise CommandError(f"CSV file not found at: {csv_path}")

        try:
            df = pd.read_csv(csv_path)
            self.stdout.write(f"Loaded {len(df)} records from {csv_path}")
        except Exception as e:
            raise CommandError(f"Error reading CSV file from {csv_path}: {e}")

        total_places_created = 0
        with transaction.atomic():
            grouped_by_city = df.groupby('city')

            for city_name, group_df in grouped_by_city:
                group_df_to_seed = group_df.head(places_per_city) 

                for index, row in group_df_to_seed.iterrows():
                    latitude = row['latitude']
                    longitude = row['longitude']
                    
                    if latitude is None or longitude is None:
                        self.stdout.write(self.style.WARNING(f"Skipping place creation in '{city_name}' due to missing geocoding data."))
                        continue

                    place_data = {
                        'name': row['name'], 
                        'description': row.get('description', ''),
                        'address': row.get('address', ''),
                        'city': row.get('city', ''),
                        'state': row.get('state', ''),
                        'country': row.get('country', ''),
                        'status': row.get('status', Status.ACTIVE), 
                        'type': row.get('type', PlaceType.CITY), 
                        'user': admin_user 
                    }

                    try:
                        place = Place(**place_data)
                        place.set_location(float(latitude), float(longitude))
                        place.save()

                        self.stdout.write(f"Created place: '{place.name}' ({row['name']}) at ({latitude}, {longitude}) for {row.get('city', '')}")
                        total_places_created += 1

                    except IntegrityError as e:
                        self.stdout.write(self.style.WARNING(f"Place '{place_data.get('name', 'Unknown')}' already exists (IntegrityError). Skipping. Error: {e}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error creating place '{place_data.get('name', 'Unknown')}': {e}"))

        self.stdout.write(self.style.SUCCESS(f"Development mode seeding completed. Total places created: {total_places_created}"))

    def _seed_production_mode(self):
        self.stdout.write("--- Seeding Places in Production Mode ---")
        self.stdout.write(self.style.WARNING("Production mode for places seeding is not implemented."))

    def handle(self, *args, **options):
        mode = options['mode']
        csv_file_relative = options['file']
        csv_path = os.path.join(settings.BASE_DIR, csv_file_relative)
        places_per_city = options['places_per_city']

        self.stdout.write(self.style.SUCCESS(f"Starting place seeding in '{mode}' mode"))

        if mode == 'development':
            self._seed_development_mode(places_per_city, csv_path)
        elif mode == 'production':
            self._seed_production_mode()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}. Use 'development' or 'production'."))

        self.stdout.write(self.style.SUCCESS("Place seeding process finished."))