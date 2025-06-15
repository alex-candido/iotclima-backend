# django_app/modules/v1/sensors/management/commands/seed_sensors.py

from django.core.management.base import BaseCommand
from faker import Faker
from django_app.modules.v1.sensors.models import Sensors

fake = Faker()


class Command(BaseCommand):
    help = 'Seed initial data for the sensors module'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=10,
            help='Number of sensors records to create',
        )

    def handle(self, *args, **options):
        total = options['total']
        self.stdout.write(f'Seeding {total} sensors items...')

        created = 0
        for _ in range(total):
            Sensors.objects.create(
                name=fake.sentence(nb_words=4)
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {created} sensors item(s).'))
