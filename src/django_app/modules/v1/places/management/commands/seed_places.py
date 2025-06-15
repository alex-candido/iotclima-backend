# django_app/modules/v1/places/management/commands/seed_places.py

import random
import re
import time

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim

from django_app.modules.v1.places.models import Place, PlaceType, Status

User = get_user_model()
fake = Faker('pt_BR')


class Command(BaseCommand):
    help = 'Seeds the database with initial place data, using real coordinates and assigning them to the admin user.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            default='development',
            help='Seeding mode: development or production (default: development)',
        )
        parser.add_argument(
            '--places_per_city',
            type=int,
            default=1,
            help='Number of places to create per city in development mode.',
        )

    def _get_cities_data(self):
        return {
            "Vale do Jaguaribe": {
                "state": "Ceará", "country": "Brazil", "cities": [
                    "Alto Santo", "Ereré", "Iracema", "Jaguaretama", "Jaguaribara",
                    "Jaguaribe", "Limoeiro do Norte", "Morada Nova", "Palhano",
                    "Pereiro", "Potiretama", "Quixeré", "Russas", "São João do Jaguaribe",
                    "Tabuleiro do Norte"
                ]},
            "Sertão dos Inhamuns": {
                "state": "Ceará", "country": "Brazil", "cities": [
                    "Aiuaba", "Arneiroz", "Parambu", "Quiterianópolis", "Tauá"
                ]},
            "Sertão de Canindé": {
                "state": "Ceará", "country": "Brazil", "cities": [
                    "Boa Viagem", "Canindé", "Caridade", "Itatira", "Madalena", "Paramoti"
                ]},
            "Maciço do Baturité": {
                "state": "Ceará", "country": "Brazil", "cities": [
                    "Acarape", "Aracoiaba", "Aratuba", "Barreira", "Baturité",
                    "Capistrano", "Guaramiranga", "Itapiúna", "Mulungu", "Ocara",
                    "Pacoti", "Palmácia", "Redenção"
                ]},
            "Litoral Oeste/Vale do Curu": {
                "state": "Ceará", "country": "Brazil", "cities": [
                    "Apuiarés", "General Sampaio", "Irauçuba", "Itapajé", "Miraíma",
                    "Pentecoste", "Tejuçuoca", "Tururu", "Umirim", "Uruburetama"
                ]},
            "Litoral Norte": {
                "state": "Ceará", "country": "Brazil", "cities": [
                    "Acaraú", "Barroquinha", "Bela Cruz", "Camocim", "Chaval",
                    "Cruz", "Granja", "Jijoca de Jericoacoara", "Marco", "Morrinhos",
                    "Uruoca", "Martinópole"
                ]},
            "Serra da Ibiapaba": {
                "state": "Ceará", "country": "Brazil", "cities": [
                    "Carnaubal", "Croatá", "Guaraciaba do Norte", "Ibiapina", "Ipu",
                    "São Benedito", "Tianguá", "Ubajara", "Viçosa do Ceará"
                ]},
            "Grande Fortaleza": {
                "state": "Ceará", "country": "Brazil", "cities": [
                    "Chorozinho", "São Luís do Curu"
                ]}
        }

    def _generate_city_abbreviation(self, city_name: str) -> str:
        cleaned_name = re.sub(r'\b(do|da|dos|das|de|di|e)\b', '', city_name, flags=re.IGNORECASE)
        cleaned_name = re.sub(r'[^a-zA-Z]', '', cleaned_name).upper()
        
        if len(cleaned_name) >= 3:
            return cleaned_name[:3]
        elif len(cleaned_name) > 0:
            return cleaned_name
        return "XXX"

    def _get_geocoded_data(self, city_name, state, country, geolocator):
        query = f"{city_name}, {state}, {country}"
        try:
            location = geolocator.geocode(query, timeout=10)
            if location:
                raw_address_dict = location.raw.get('address', {})
                formatted_full_address = location.raw.get('display_name', query)

                canonical_city_name = raw_address_dict.get('city') or raw_address_dict.get('town') or city_name

                country_code = raw_address_dict.get('country_code', 'BR').upper()
                state_abbr = raw_address_dict.get('state_abbr', state[:2].upper())
                derived_place_code = f"{country_code}-{state_abbr}-{self._generate_city_abbreviation(canonical_city_name)}"
                
                return location.latitude, location.longitude, raw_address_dict, canonical_city_name, derived_place_code, formatted_full_address
            
            self.stdout.write(self.style.WARNING(f"Warning: No geocoding result for '{query}'."))
            return None, None, {}, None, None, None
        
        except GeocoderTimedOut:
            self.stdout.write(self.style.ERROR(f"Error: Geocoding service timed out for '{query}'. Retrying in 1 second."))
            time.sleep(1)
            return self._get_geocoded_data(city_name, state, country, geolocator)
        except GeocoderServiceError as e:
            self.stdout.write(self.style.ERROR(f"Error: Geocoding service error for '{query}': {e}. Skipping city."))
            return None, None, {}, None, None, None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred during geocoding for '{query}': {e}. Skipping city."))
            return None, None, {}, None, None, None

    def _seed_development_mode(self, places_per_city):
        self.stdout.write("--- Seeding Places in Development Mode ---")

        all_cities_data = self._get_cities_data()
        
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                raise CommandError("No superuser found. Please ensure a superuser exists (e.g., run 'python manage.py createsuperuser' or 'seed_users').")
        except Exception as e:
            raise CommandError(f"Error fetching superuser: {e}")

        geolocator = Nominatim(user_agent="iotclima_seed_places_v3")
        
        total_places_created = 0
        with transaction.atomic():
            for region, data in all_cities_data.items():
                state = data['state']
                country = data['country']
                for city_name_full in data['cities']:
                    latitude, longitude, raw_address_dict, canonical_city_name, derived_place_code, formatted_full_address = self._get_geocoded_data(city_name_full, state, country, geolocator)
                    time.sleep(1.1)

                    if latitude is None or longitude is None:
                        self.stdout.write(self.style.WARNING(f"Skipping place creation in '{city_name_full}' due to missing geocoding data."))
                        continue

                    if isinstance(raw_address_dict, dict):
                        address_parts = [
                            raw_address_dict.get('road'),
                            raw_address_dict.get('house_number'),
                            raw_address_dict.get('suburb'),
                            raw_address_dict.get('city') or raw_address_dict.get('town'),
                            raw_address_dict.get('state'),
                            raw_address_dict.get('postcode'),
                            raw_address_dict.get('country')
                        ]
                        formatted_address = ", ".join(filter(None, address_parts))
                    else: 
                        formatted_address = formatted_full_address 

                    if not formatted_address: 
                        formatted_address = f"{city_name_full}, {state}, {country}"

                    for i in range(places_per_city):
                        place_data = {
                            'name': f"{derived_place_code}_{i+1}",
                            'description': f"Meteorological station located in {canonical_city_name}, {state}, {country}. Georeferenced location.",
                            'address': formatted_address,
                            'city': canonical_city_name,
                            'state': state,
                            'country': country,
                            'status': Status.ACTIVE,
                            'type': PlaceType.CITY,
                            'user': admin_user
                        }
                        
                        place = Place(**place_data)
                        place.set_location(float(latitude), float(longitude))
                        place.save()

                        self.stdout.write(f"Created place: '{place.name}' ({derived_place_code}) at ({latitude}, {longitude}) for {canonical_city_name}")
                        total_places_created += 1

        self.stdout.write(self.style.SUCCESS(f"Development mode seeding completed. Total places created: {total_places_created}"))

    def _seed_production_mode(self):
        self.stdout.write("--- Seeding Places in Production Mode ---")
        self.stdout.write(self.style.WARNING("Production mode for places seeding is not implemented. Please add specific logic if needed."))

    def handle(self, *args, **options):
        mode = options['mode']
        places_per_city = options['places_per_city']

        self.stdout.write(self.style.SUCCESS(f"Starting place seeding in '{mode}' mode"))

        if mode == 'development':
            self._seed_development_mode(places_per_city)
        elif mode == 'production':
            self._seed_production_mode()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}. Use 'development' or 'production'."))

        self.stdout.write(self.style.SUCCESS("Place seeding process finished."))