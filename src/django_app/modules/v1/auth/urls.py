# django_app/modules/v1/auth/urls.py

from django.urls import path, re_path
from django.views.generic import TemplateView
from allauth.account.views import ConfirmEmailView 

from .api import (
    # JWT Authentication views
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
    # Authentication views
    LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, UserDetailsView,
    # Registration views
    RegisterView, VerifyEmailView, ResendEmailVerificationView
)

urlpatterns = [
    # Authentication endpoints
    # URLs that do not require a session or valid token
    re_path(r'login/?$', LoginView.as_view(), name='rest_login'),
    re_path(r'^password/reset/?$', PasswordResetView.as_view(), name='rest_password_reset'),
    re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  
    # URLs that require a user to be logged in with a valid session / token.
    re_path(r'logout/?$', LogoutView.as_view(), name='rest_logout'),
    re_path(r'user/?$', UserDetailsView.as_view(), name='rest_user_details'),
    re_path(r'password/change/?$', PasswordChangeView.as_view(), name='rest_password_change'),

    # Registration endpoints
    re_path(r'^registration/?$', RegisterView.as_view(), name='rest_register'),
    re_path(r'^registration/verify-email/?$', VerifyEmailView.as_view(), name='rest_verify_email'),
    re_path(r'^registration/resend-email/?$', ResendEmailVerificationView.as_view(), name='rest_resend_email'),
    re_path(r'^registration/account-confirm-email/(?P<key>[-:\w]+)/?$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    re_path(r'^registration/account-email-verification-sent/?$', TemplateView.as_view(), name='account_email_verification_sent'),

    # JWT Authentication endpoints
    re_path(r'^token/?$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/verify/?$', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^token/refresh/?$', TokenRefreshView().as_view(), name='token_refresh'),
]
