# django_app/modules/v1/station_sensors/management/commands/seed_station_sensors.py

import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from faker import Faker

from django_app.modules.v1.sensors.models import Sensor, SensorType, UnitType
from django_app.modules.v1.station_sensors.models import StationSensor
from django_app.modules.v1.stations.models import Station

User = get_user_model()
fake = Faker('en_US')

SENSOR_LINK_PROPERTIES = {
    SensorType.TEMPERATURE: {'position_options': ["Top", "Mid", "External"], 'cal_at_range': ('-6m', 'now')},
    SensorType.HUMIDITY:    {'position_options': ["Mid", "Internal", "Sheltered"], 'cal_at_range': ('-9m', 'now')},
    SensorType.WIND:        {'position_options': ["High Pole", "Mast Top"], 'cal_at_range': ('-1y', '-3m')},
    SensorType.PRESSURE:    {'position_options': ["Internal", "Ground Level"], 'cal_at_range': ('-1y', '-6m')},
    SensorType.RAINFALL:    {'position_options': ["Ground Level", "Rain Collector"], 'cal_at_range': ('-6m', 'now')},
}

class Command(BaseCommand):
    help = 'Seeds the database with StationSensor links, associating 5 types of sensors to each station.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            default='development',
            help='Seeding mode: development or production (default: development)',
        )

    def _seed_development_mode(self):
        self.stdout.write("--- Seeding StationSensor Links in Development Mode ---")

        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                raise CommandError("Admin user not found. Please run 'python manage.py seed_users' first.")
        except Exception as e:
            raise CommandError(f"Error fetching superuser: {e}")

        all_stations = list(Station.objects.all())
        if not all_stations:
            raise CommandError("No stations found. Please run 'python manage.py seed_stations' first to create stations.")
        
        all_sensors_by_type = {
            sensor_type: list(Sensor.objects.filter(type=sensor_type))
            for sensor_type in list(SensorType.values) if sensor_type != SensorType.OTHER
        }

        for sensor_type_value in [st for st in SensorType.values if st != SensorType.OTHER]:
            if not all_sensors_by_type.get(sensor_type_value):
                raise CommandError(f"No sensors of type '{SensorType(sensor_type_value).label}' found. Please run 'python manage.py seed_sensors' first.")


        total_links_created = 0
        with transaction.atomic():
            for station in all_stations:
                self.stdout.write(f"Processing Station: {station.name}")
                
                for sensor_type_value in [st for st in SensorType.values if st != SensorType.OTHER]:
                    sensor_pool = all_sensors_by_type[sensor_type_value]
                    if not sensor_pool: continue
                    sensor_to_link = random.choice(sensor_pool)

                    link_properties = SENSOR_LINK_PROPERTIES.get(sensor_type_value, {})
                    
                    installed_date_naive = fake.date_time_between(
                        start_date='-2y', end_date='-1y'
                    )
                    installed_date_aware = timezone.make_aware(installed_date_naive)
                    
                    calibrated_at_aware = None
                    if link_properties.get('cal_at_range'):
                        cal_start, cal_end = link_properties['cal_at_range']
                        calibrated_at_naive = fake.date_time_between(start_date=cal_start, end_date=cal_end)
                        calibrated_at_aware = timezone.make_aware(calibrated_at_naive)


                    link_data = {
                        'station': station,
                        'sensor': sensor_to_link,
                        'installed_date': installed_date_aware,
                        'position': random.choice(link_properties.get('position_options', ['Default Position'])),
                        'is_active': True,
                        'calibrated_at': calibrated_at_aware,
                        'removed_date': None,
                    }

                    try:
                        existing_link = station.station_sensor_links.filter(sensor=sensor_to_link).first() # type: ignore
                        if existing_link:
                            self.stdout.write(self.style.WARNING(f"Link for Station '{station.name}' and Sensor '{sensor_to_link.model}' already exists. Skipping."))
                            continue

                        link = StationSensor(**link_data)
                        link.save()

                        self.stdout.write(f"Created link: Station '{station.name}' <-> Sensor '{sensor_to_link.model}' (Type: {sensor_to_link.get_type_display()}) at '{link.position}'") # type: ignore
                        total_links_created += 1

                    except IntegrityError as e:
                        self.stdout.write(self.style.WARNING(f"Integrity Error for Station '{station.name}' <-> Sensor '{sensor_to_link.model}': {e}. Skipping."))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error creating link for Station '{station.name}' <-> Sensor '{sensor_to_link.model}': {e}"))

        self.stdout.write(self.style.SUCCESS(f"Development mode seeding completed. Total StationSensor links created: {total_links_created}"))


    def _seed_production_mode(self):
        self.stdout.write("--- Seeding StationSensor Links in Production Mode ---")
        self.stdout.write(self.style.WARNING("Production mode for StationSensor links seeding is not implemented. Please add specific logic if needed."))

    def handle(self, *args, **options):
        mode = options['mode']

        self.stdout.write(self.style.SUCCESS(f"--- Starting StationSensor Seeding in '{mode}' Mode ---"))

        if mode == 'development':
            self._seed_development_mode()
        elif mode == 'production':
            self._seed_production_mode()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}. Use 'development' or 'production'."))

        self.stdout.write(self.style.SUCCESS("StationSensor seeding process finished."))