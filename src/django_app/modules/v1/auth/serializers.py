# django_app/modules/v1/auth/serializers.py

from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.serializers import PasswordResetSerializer
from django.conf import settings


def custom_url_generator(request, user, temp_key):
    uid = user_pk_to_url_str(user)
    return f'{settings.ACCOUNT_PASSWORD_REDIRECT_URL}/{uid}/{temp_key}/'

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {
          'url_generator': custom_url_generator
        }        
        
        