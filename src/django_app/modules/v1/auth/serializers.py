# django_app/modules/v1/auth/serializers.py

from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.registration.serializers import \
    RegisterSerializer as DefaultRegisterSerializer
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
from django.contrib.auth.models import Group
from rest_framework import serializers


def custom_url_generator(request, user, temp_key):
    uid = user_pk_to_url_str(user)
    return f'{settings.ACCOUNT_PASSWORD_REDIRECT_URL}/{uid}/{temp_key}/'

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {
          'url_generator': custom_url_generator
        }        
        
class CustomLoginSerializer(DefaultLoginSerializer):
    pass

class CustomRegisterSerializer(DefaultRegisterSerializer):
    def save(self, request):
        user = super().save(request)
        try:
            customer_group = Group.objects.get(name='CUSTOMER')
            user.groups.add(customer_group)

        except Group.DoesNotExist:
            print("WARNING: 'CUSTOMER' group not found. User not assigned to default group.")
        
        return user