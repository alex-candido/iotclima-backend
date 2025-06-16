# django_app/modules/v1/users/serializers.py

from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from dj_rest_auth.serializers import \
    UserDetailsSerializer as DefaultUserDetailsSerializer
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from .models import User


class UsersInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)


class UsersOutputSerializer(serializers.ModelSerializer):
    group_names = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'uuid', 'username', 'first_name', 'last_name', 'email',
            'is_superuser', 'is_staff', 'is_active',
            'date_joined', 'last_login', 'created_at', 'updated_at',
            'group_names',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_group_names(self, obj):
        return [group.name for group in obj.groups.all()]


class CustomUserDetailsSerializer(DefaultUserDetailsSerializer):
    group_names = serializers.SerializerMethodField()

    class Meta(DefaultUserDetailsSerializer.Meta):
        fields = DefaultUserDetailsSerializer.Meta.fields + ('group_names',) 


    def get_group_names(self, obj):
        return [group.name for group in obj.groups.all()]
