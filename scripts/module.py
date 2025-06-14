import os
import re
import shutil
from typing import Any, Dict, List

from colorama import Fore, Style, init

# Conteúdo base para os arquivos do módulo, com placeholders
MODULE_FILES_CONTENT = {
    "__init__.py": "",
    "admin.py": """from django.contrib import admin
from .models import {class_name}

@admin.register({class_name})
class {class_name}Admin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'name', 'created_at', 'updated_at')
    search_fields = ('id', 'uuid', 'name')
    ordering = ('-created_at',)
""",
    "api.py": """from typing import Type, Union, Any, List
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from django_app.container import core_container

from .serializers import {class_name}InputSerializer, {class_name}OutputSerializer
from .services import {class_name}Service


class {class_name}ViewSet(viewsets.ViewSet):
    service: {class_name}Service = core_container.{module_name}_container.service()

    @staticmethod
    def _validated_data(serializer_class: Type[Serializer], data: Union[dict, List[dict], Any], **kwargs) -> Any:
        serializer = serializer_class(data=data, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @staticmethod
    def _to_response(serializer_class: Type[Serializer], output: Union[dict, List[dict], Any], **kwargs) -> Union[dict, List[dict], Any]:
        serializer = serializer_class(output, **kwargs)
        return serializer.data

    # GET /{module_name}/
    def list(self, request):
        output = self.service.list()
        data = self._to_response({class_name}OutputSerializer, output, many=True)
        return Response(data)

    # POST /{module_name}/
    def create(self, request):
        input_data = self._validated_data({class_name}InputSerializer, data=request.data)
        output = self.service.create(input_data)
        data = self._to_response({class_name}OutputSerializer, output)
        return Response(data, status=status.HTTP_201_CREATED)

    # GET /{module_name}/{{pk}}/
    def retrieve(self, request, pk=None):
        output = self.service.retrieve(pk)
        data = self._to_response({class_name}OutputSerializer, output)
        return Response(data)

    # PUT /{module_name}/{{pk}}/
    def update(self, request, pk=None):
        input_data = self._validated_data({class_name}InputSerializer, data=request.data)
        output = self.service.update(pk, input_data)
        data = self._to_response({class_name}OutputSerializer, output)
        return Response(data)

    # PATCH /{module_name}/{{pk}}/
    def partial_update(self, request, pk=None):
        instance = self.service.get_instance(pk)
        input_data = self._validated_data({class_name}InputSerializer, data=request.data, instance=instance, partial=True)
        output = self.service.update(pk, input_data)
        data = self._to_response({class_name}OutputSerializer, output)
        return Response(data)

    # DELETE /{module_name}/{{pk}}/
    def destroy(self, request, pk=None):
        self.service.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
""",
    "apps.py": """from django.apps import AppConfig


class {class_name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app_full_name}'
    label = '{module_name}'
    verbose_name = '{class_name}'
""",
    "models.py": """from django.db import models
import uuid


class {class_name}(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
{model_fields}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
""",
    "repositories.py": """from .models import {class_name}


class {class_name}Repository:

    def list(self):
        return {class_name}.objects.all()

    def create(self, validated_data):
        return {class_name}.objects.create(**validated_data)

    def get(self, pk):
        return {class_name}.objects.get(pk=pk)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
""",
    "serializers.py": """from rest_framework import serializers
from .models import {class_name}


class {class_name}InputSerializer(serializers.Serializer):
{serializer_input_fields}


class {class_name}OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = {class_name}
        fields = '__all__'
""",
    "services.py": """
from .repositories import {class_name}Repository


class {class_name}Service:
    def __init__(self, repository: {class_name}Repository):
        self.repository = repository

    def list(self):
        return self.repository.list()

    def create(self, input_data):
        return self.repository.create(input_data)

    def retrieve(self, pk):
        return self.repository.get(pk)

    def update(self, pk, input_data):
        instance = self.repository.get(pk)
        return self.repository.update(instance, input_data)

    def delete(self, pk):
        instance = self.repository.get(pk)
        self.repository.delete(instance)

    def get_instance(self, pk):
        return self.repository.get(pk)
""",
    "tests.py": """from django.test import TestCase


class {class_name}Tests(TestCase):
    def test_example(self):
        self.assertTrue(True)
""",
    "urls.py": """from rest_framework.routers import DefaultRouter
from .api import {class_name}ViewSet

router = DefaultRouter()
router.register(r'', {class_name}ViewSet, basename='{module_name}')

urlpatterns = router.urls
""",
    "views.py": """from django.shortcuts import render

# Create your views here.
""",
    "migrations/__init__.py": "",
    "management/commands/seed_{module_name}.py": """from django.core.management.base import BaseCommand
from faker import Faker
from django_app.modules.v1.{module_name}.models import {class_name}

fake = Faker()


class Command(BaseCommand):
    help = 'Seed initial data for the {module_name} module'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=10,
            help='Number of {module_name} records to create',
        )

    def handle(self, *args, **options):
        total = options['total']
        self.stdout.write(f'Seeding {{total}} {module_name} items...')

        created = 0
        for _ in range(total):
            {class_name}.objects.create(
                name=fake.sentence(nb_words=4)
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {{created}} {module_name} item(s).'))
""",
    "container.py": """from dependency_injector import containers, providers

from .repositories import {class_name}Repository
from .services import {class_name}Service


class {class_name}Container(containers.DeclarativeContainer):
    repository = providers.Factory({class_name}Repository)
    service = providers.Factory({class_name}Service, repository=repository)
""",
}

# Inicializa colorama para cores no terminal
init(autoreset=True)


# Funções para print colorido
def print_success(msg):
    print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}")


def print_warning(msg):
    print(f"{Fore.YELLOW}WARNING: {msg}{Style.RESET_ALL}")


def print_error(msg):
    print(f"{Fore.RED}ERROR: {msg}{Style.RESET_ALL}")


def print_removed(msg):
    print(f"{Fore.MAGENTA}REMOVED: {msg}{Style.RESET_ALL}")


def get_header_comment(path):
    return f"# {path}\n\n"


def to_pascal_case(snake_str: str) -> str:
    return ''.join(word.capitalize() for word in snake_str.split('_'))


def add_route_to_routes_py(routes_path, version, module_name):
    route_line = f"    path('{module_name}/', include('django_app.modules.{version}.{module_name}.urls')),"
    with open(routes_path, "r+", encoding="utf-8") as f:
        content = f.read()
        if route_line in content:
            return
        insert_pos = content.find("urlpatterns = [")
        if insert_pos == -1:
            print_warning(f"Cannot find urlpatterns list in {routes_path}")
            return
        bracket_pos = content.find("[", insert_pos)
        content = content[:bracket_pos + 1] + "\n" + route_line + content[bracket_pos + 1:]
        f.seek(0)
        f.write(content)
        f.truncate()


def add_app_to_settings(settings_path, version, module_name):
    app_line = f"    'django_app.modules.{version}.{module_name}',"
    with open(settings_path, "r+", encoding="utf-8") as f:
        content = f.read()
        if app_line in content:
            return
        insert_pos = content.find("INSTALLED_APPS")
        if insert_pos == -1:
            print_warning(
                f"Cannot find INSTALLED_APPS list in {settings_path}")
            return
        bracket_pos = content.find("[", insert_pos)
        end_bracket = content.find("]", bracket_pos)
        content = content[:end_bracket] + "\n" + \
            app_line + "\n" + content[end_bracket:]
        f.seek(0)
        f.write(content)
        f.truncate()


def remove_line_containing(file_path, text):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(file_path, "w", encoding="utf-8") as f:
        for line in lines:
            if text not in line:
                f.write(line)


def generate_http_file_content(version: str, module_name: str) -> str:
    return f"""# http/{version}_{module_name}.http

@baseUrl = http://localhost:3333/api/v1
@{module_name}_id = 1

### List all {module_name}
GET {{baseUrl}}/{module_name}/

### Create a new {module_name}
POST {{baseUrl}}/{module_name}/
Content-Type: application/json

{{
  "name": "Sample {module_name} name"
}}

### Retrieve a {module_name} by ID
GET {{baseUrl}}/{module_name}/{{{{{module_name}_id}}}}/

### Update a {module_name} by ID (PUT)
PUT {{baseUrl}}/{module_name}/{{{{{module_name}_id}}}}/
Content-Type: application/json

{{
  "name": "Updated {module_name} name"
}}

### Partially update a {module_name} by ID (PATCH)
PATCH {{baseUrl}}/{module_name}/{{{{{module_name}_id}}}}/
Content-Type: application/json

{{
  "name": "Partial update of {module_name} name"
}}

### Delete a {module_name} by ID
DELETE {{baseUrl}}/{module_name}/{{{{{module_name}_id}}}}/
"""


def generate_model_fields_code(fields):
    lines = []
    for field in fields:
        params = field["params"]
        model_kwargs = []

        for param_name, param_value in params.items():
            if param_name == 'max_length':
                model_kwargs.append(f'max_length={param_value}')
            elif param_name == 'max_digits':
                model_kwargs.append(f'max_digits={param_value}')
            elif param_name == 'decimal_places':
                model_kwargs.append(f'decimal_places={param_value}')
            elif param_name == 'default':
                model_kwargs.append(f'default={repr(param_value)}')
            elif param_name == 'null' and param_value is True:
                model_kwargs.append('null=True')

        kwargs_str = ', '.join(model_kwargs)
        lines.append(f"    {field['name']} = models.{field['type']}({kwargs_str})")
    return "\n".join(lines)


def generate_serializer_fields_code(fields):
    lines = []
    for field in fields:
        if field["type"] == "CharField":
            max_length = field["params"].get("max_length", "255")
            lines.append(
                f"    {field['name']} = serializers.CharField(max_length={max_length})")
        elif field["type"] == "BooleanField":
            lines.append(f"    {field['name']} = serializers.BooleanField()")
        elif field["type"] == "IntegerField":
            lines.append(f"    {field['name']} = serializers.IntegerField()")
        elif field["type"] == "DecimalField":
            lines.append(
                f"    {field['name']} = serializers.DecimalField(max_digits={field['params'].get('max_digits')}, decimal_places={field['params'].get('decimal_places')})")
        else:
            lines.append(
                f"    {field['name']} = serializers.CharField()  # Tipo {field['type']} não reconhecido")
    return "\n".join(lines)


def create_module(base_dir, app_name, version, module_name, fields=None):
    base_module_path = os.path.join(
        base_dir, app_name, "modules", version, module_name)
    if os.path.exists(base_module_path):
        print_warning(f"Module '{module_name}' already exists at {base_module_path}")
        return

    os.makedirs(base_module_path, exist_ok=True)
    os.makedirs(os.path.join(base_module_path, "migrations"), exist_ok=True)
    os.makedirs(os.path.join(base_module_path, "management", "commands"),
                exist_ok=True)

    class_name = to_pascal_case(module_name)
    app_full_name = f"{app_name}.modules.{version}.{module_name}"

    if not fields:
        fields_list = [{"name": "name", "type": "CharField",
                        "params": {"max_length": 255}}]
    else:
        fields_list = fields

    for file_path, content_template in MODULE_FILES_CONTENT.items():
        file_actual = file_path.replace("{module_name}", module_name)
        full_path = os.path.join(base_module_path, file_actual)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        relative_path = os.path.relpath(full_path,
                                        base_dir).replace("\\", "/")
        header = get_header_comment(relative_path)

        content = content_template.format(
            module_name=module_name,
            class_name=class_name,
            app_full_name=app_full_name,
            model_fields=generate_model_fields_code(
                fields_list) if file_path == "models.py" else "",
            serializer_input_fields=generate_serializer_fields_code(
                fields_list) if file_path == "serializers.py" else ""
        )

        full_content = header + content

        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(full_content)
            print_success(f"Created: {relative_path}")
        else:
            print_warning(f"Already exists: {relative_path}")

    add_route_to_routes_py(
        os.path.join(base_dir, app_name, "routes.py"), version, module_name)
    add_app_to_settings(
        os.path.join(base_dir, app_name, "settings.py"), version, module_name)
    
    update_core_container(base_dir, app_name, module_name)

    # Criação do arquivo http
    http_dir = os.path.join("http")
    os.makedirs(http_dir, exist_ok=True)

    http_file_path = os.path.join(http_dir, f"{version}_{module_name}.http")
    if not os.path.exists(http_file_path):
        http_content = generate_http_file_content(version, module_name)
        with open(http_file_path, "w", encoding="utf-8") as f:
            f.write(http_content)
        print_success(f"Created: http/{version}_{module_name}.http")
    else:
        print_warning(f"Already exists: http/{version}_{module_name}.http")



def remove_module(base_dir, app_name, version, module_name):
    base_module_path = os.path.join(
        base_dir, app_name, "modules", version, module_name)
    http_filename = f"{version}_{module_name}.http"
    http_path = os.path.join("http", http_filename)

    if not os.path.exists(base_module_path):
        print_warning(f"Module '{module_name}' does not exist.")
        return

    if os.path.exists(http_path):
        os.remove(http_path)
    shutil.rmtree(base_module_path)
    print_removed(f"Removed module '{module_name}' at {base_module_path}")

    routes_path = os.path.join(base_dir, app_name, "routes.py")
    module_import_path = f"django_app.modules.{version}.{module_name}"
    remove_line_containing(routes_path, module_import_path)

    settings_path = os.path.join(base_dir, app_name, "settings.py")
    app_line = f"'{module_import_path}',"
    remove_line_containing(settings_path, app_line)
    
    update_core_container_removal(base_dir, app_name, module_name)
    
def update_core_container_removal(base_dir, app_name, module_name):
    container_path = os.path.join(base_dir, app_name, "container.py")
    class_name = to_pascal_case(module_name)
    module_container_name = f"{module_name}_container"
    import_line = f"from .modules.v1.{module_name}.container import {class_name}Container"
    container_assignment = f"    {module_container_name} = providers.Container({class_name}Container)"

    with open(container_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    removed_import = False
    removed_assignment = False

    for line in lines:
        if not removed_import and import_line in line:
            removed_import = True
        elif not removed_assignment and container_assignment in line:
            removed_assignment = True
        else:
            updated_lines.append(line)

    with open(container_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

def update_core_container(base_dir, app_name, module_name):
    container_path = os.path.join(base_dir, app_name, "container.py")
    class_name = to_pascal_case(module_name)
    module_container_name = f"{module_name}_container"
    import_line = f"from .modules.v1.{module_name}.container import {class_name}Container"
    container_assignment = f"    {module_container_name} = providers.Container({class_name}Container)"

    # Read the existing content of the container.py file
    with open(container_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if the import line already exists
    if import_line not in content:
        # Find the position to insert the import (after other imports)
        import_insert_position = content.find("from dependency_injector import")
        if import_insert_position != -1:
            # Insert the new import line
            content = content[:import_insert_position] + import_line + "\n" + content[import_insert_position:]
        else:
            print_warning(f"Could not find insertion point for import in {container_path}")
            return

    # Check if the container assignment already exists
    if container_assignment not in content:
        # Find the position to insert the container assignment (inside the CoreContainer class)
        class_start_position = content.find("class CoreContainer(containers.DeclarativeContainer):")
        if class_start_position != -1:
            # Find the first line inside the class
            first_line_position = content.find("\n", class_start_position) + 1
            # Insert the container assignment
            content = content[:first_line_position] + container_assignment + "\n" + content[first_line_position:]
        else:
            print_warning(f"Could not find insertion point for container assignment in {container_path}")
            return

    # Write the modified content back to the container.py file
    with open(container_path, "w", encoding="utf-8") as f:
        f.write(content)
    print_success(f"Updated {container_path} to include {module_container_name}")

