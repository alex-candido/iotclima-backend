# django_app/modules/v1/users/management/commands/seed_users.py

import random

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

# from django.contrib.auth.models import Permission # Permissions and ContentType are commented out as requested
# from django.contrib.contenttypes.models import ContentType

User = get_user_model()
fake = Faker('en_US')

class Command(BaseCommand):
    help = 'Seeds the database with initial user, group, and permission data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            default='development',
            help='Seeding mode: development or production (default: development)',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of additional fake users to create (only in development mode). These will be distributed among MANAGER, OPERATOR, EMPLOYEE, CUSTOMER, VIEWER groups.',
        )

    # --- Utility Methods for User Data ---
    def _create_user_data_dict(self, username, email, password, first_name, last_name, is_staff=False, is_superuser=False, is_active=True):
        """Creates a dictionary for user data."""
        return {
            'username': username, 'email': email, 'password': password,
            'first_name': first_name, 'last_name': last_name,
            'is_staff': is_staff, 'is_superuser': is_superuser, 'is_active': is_active
        }

    def _get_admin_user_data(self):
        """Returns data for the primary admin user (superuser, Django Admin access)."""
        return self._create_user_data_dict('admin', 'admin@example.com', 'Admin@123', 'System', 'Administrator', True, True, True)

    def _get_test_user_data(self):
        """Returns data for a generic test user (Main App access)."""
        return self._create_user_data_dict('testuser', 'test@example.com', 'Test@123', 'Test', 'User', False, False, True)

    def _get_owner_user_data(self):
        """Returns data for an OWNER type user (Frontend Admin/App access)."""
        return self._create_user_data_dict(fake.unique.user_name(), fake.unique.email(), 'Owner@123', fake.first_name(), fake.last_name(), False, False, True)

    def _get_manager_user_data(self):
        """Returns data for a MANAGER type user (Frontend Admin/App access)."""
        return self._create_user_data_dict(fake.unique.user_name(), fake.unique.email(), 'Manager@123', fake.first_name(), fake.last_name(), False, False, True)

    def _get_operator_user_data(self):
        """Returns data for an OPERATOR type user (Frontend Admin/App access)."""
        return self._create_user_data_dict(fake.unique.user_name(), fake.unique.email(), 'Operator@123', fake.first_name(), fake.last_name(), False, False, True)

    def _get_employee_user_data(self):
        """Returns data for an EMPLOYEE type user (Frontend Admin/App access)."""
        return self._create_user_data_dict(fake.unique.user_name(), fake.unique.email(), 'Employee@123', fake.first_name(), fake.last_name(), False, False, True)

    def _get_customer_user_data(self):
        """Returns data for a CUSTOMER type user (Main App access)."""
        return self._create_user_data_dict(fake.unique.user_name(), fake.unique.email(), 'Customer@123', fake.first_name(), fake.last_name(), False, False, True)

    def _get_viewer_user_data(self):
        """Returns data for a VIEWER type user (Frontend Admin/Dashboard read-only access)."""
        return self._create_user_data_dict(fake.unique.user_name(), fake.unique.email(), 'Viewer@123', fake.first_name(), fake.last_name(), False, False, True)

    # --- Core Seeding Logic for Users, Groups, Permissions ---
    def _create_user_with_hashed_password(self, user_data: dict):
        """Creates or retrieves a user, sets password, and ensures EmailAddress is created."""
        username = user_data['username']
        password = user_data.pop('password') # Get password and remove it from dict

        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f"User '{username}' already exists. Skipping creation."))
            return user
        except User.DoesNotExist:
            self.stdout.write(f"Creating user: {username}")
            
            # Create user instance with remaining data
            user = User(**user_data) 
            user.set_password(password) # Hash and set password
            user.save() # Save user with hashed password

            # Ensure EmailAddress is created and verified for allauth
            EmailAddress.objects.get_or_create(
                user=user,
                email=user.email,
                verified=True,
                primary=True,
            )
            self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))
            return user

    def _seed_groups(self):
        """Seeds standard user groups."""
        self.stdout.write("--- Seeding Groups ---")
        group_names = ['ADMIN', 'OWNER', 'MANAGER', 'OPERATOR', 'EMPLOYEE', 'CUSTOMER', 'VIEWER']
        created_groups = {}
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            created_groups[name] = group
            self.stdout.write(f'{"Created" if created else "Found"} group: {name}')
        return created_groups

    # # --- Permissions Seeding (Commented out as per request) ---
    # def _seed_permissions(self):
    #     """Seeds custom permissions. Currently creates them without ContentType."""
    #     self.stdout.write("--- Seeding Permissions ---")
    #     permissions_data = [
    #         ('add_station', 'Can add station'), ('change_station', 'Can change station'),
    #         ('delete_station', 'Can delete station'), ('view_station', 'Can view station'),
    #         ('add_sensor', 'Can add sensor'), ('change_sensor', 'Can change sensor'),
    #         ('delete_sensor', 'Can delete sensor'), ('view_sensor', 'Can view sensor'),
    #         ('add_place', 'Can add place'), ('change_place', 'Can change place'),
    #         ('delete_place', 'Can delete place'), ('view_place', 'Can view place'),
    #         ('view_reports', 'Can view reports'),
    #         ('manage_events', 'Can manage events'),
    #     ]
    #     created_permissions = []
    #     for codename, name in permissions_data:
    #         permission, created = Permission.objects.get_or_create(
    #             codename=codename,
    #             content_type=None, # Set to None, as related models are not available in current structure
    #             defaults={'name': name}
    #         )
    #         created_permissions.append(permission)
    #         self.stdout.write(f'{"Created" if created else "Found"} permission: {codename}')
    #     return created_permissions

    # def _assign_permissions_to_admin_group(self, created_groups, created_permissions):
    #     """Assigns all created custom permissions to the ADMIN group."""
    #     self.stdout.write("--- Assigning Permissions to ADMIN Group ---")
    #     admin_group = created_groups['ADMIN']
    #     for permission in created_permissions:
    #         admin_group.permissions.add(permission)
    #     self.stdout.write('All custom permissions assigned to ADMIN group.')

    def _seed_development_mode(self, count):
        """Seeds users, groups, and (optionally) permissions for development environment."""
        created_groups = self._seed_groups()
        # Permissions are skipped as per request. Uncomment if needed later.
        # created_permissions = self._seed_permissions()
        # self._assign_permissions_to_admin_group(created_groups, created_permissions)

        self.stdout.write(f"--- Seeding Users in Development Mode ---")

        with transaction.atomic():
            # --- Create specific users and assign to groups ---
            # ADMIN User (Superuser, sole Django Admin access)
            admin_user = self._create_user_with_hashed_password(self._get_admin_user_data())
            admin_user.groups.add(created_groups['ADMIN'])
            self.stdout.write(f"Assigned '{admin_user.username}' to 'ADMIN' group (Django Admin access).")

            # TEST User (Example: assigned to CUSTOMER, Main App access)
            test_user = self._create_user_with_hashed_password(self._get_test_user_data())
            test_user.groups.add(created_groups['CUSTOMER'])
            self.stdout.write(f"Assigned '{test_user.username}' to 'CUSTOMER' group (Main App access).")

            # OWNER User (Unique, Frontend Admin/App access)
            owner_user = self._create_user_with_hashed_password(self._get_owner_user_data())
            owner_user.groups.add(created_groups['OWNER'])
            self.stdout.write(f"Assigned '{owner_user.username}' to 'OWNER' group (Frontend Admin/App access).")
            
            # --- Create multiple users for other groups ---
            # Distribute 'count' users among these groups, ensuring at least one per group
            multiple_user_groups_configs = {
                'MANAGER': {'data_func': self._get_manager_user_data},
                'OPERATOR': {'data_func': self._get_operator_user_data},
                'EMPLOYEE': {'data_func': self._get_employee_user_data},
                'CUSTOMER': {'data_func': self._get_customer_user_data},
                'VIEWER': {'data_func': self._get_viewer_user_data},
            }

            users_per_multiple_group = max(1, count // len(multiple_user_groups_configs))

            for group_name, config in multiple_user_groups_configs.items():
                self.stdout.write(f"Creating {users_per_multiple_group} users for group: {group_name}")
                for _ in range(users_per_multiple_group):
                    user_data = config['data_func']()
                    user = self._create_user_with_hashed_password(user_data)
                    user.groups.add(created_groups[group_name])
                    self.stdout.write(f"Assigned '{user.username}' to '{group_name}' group.")
        
        self.stdout.write(self.style.SUCCESS("Development mode seeding completed."))

    def _seed_production_mode(self):
        """Seeds essential users and groups for production environment."""
        created_groups = self._seed_groups()
        # Permissions are skipped as per request. Uncomment if needed later.
        # created_permissions = self._seed_permissions()
        # self._assign_permissions_to_admin_group(created_groups, created_permissions)

        admin_data = self._get_admin_user_data()

        self.stdout.write("--- Seeding Admin User in Production Mode ---")
        with transaction.atomic():
            admin_user = self._create_user_with_hashed_password(admin_data)
            admin_user.groups.add(created_groups['ADMIN'])
            self.stdout.write(self.style.SUCCESS(f"Production mode seeding completed for Admin user."))

    # --- Main handle method ---
    def handle(self, *args, **options):
        """Main entry point for the seed command."""
        mode = options['mode']
        count = options['count']

        self.stdout.write(self.style.SUCCESS(f"Starting user seeding in '{mode}' mode"))

        if mode == 'development':
            self._seed_development_mode(count)
        elif mode == 'production':
            self._seed_production_mode()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown mode: {mode}. Use 'development' or 'production'."))

        self.stdout.write(self.style.SUCCESS("User seeding process finished."))