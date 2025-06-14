# django_app/modules/v1/users/serializers.py

from rest_framework import serializers

from .models import User


class UsersInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.CharField()  
    password = serializers.CharField(max_length=128)

class UsersOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
