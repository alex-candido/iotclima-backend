# django_app/modules/v1/auth/api.py

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, UserDetailsView, PasswordResetView, PasswordResetConfirmView
from dj_rest_auth.registration.views import (
    RegisterView,
    VerifyEmailView,
    ResendEmailVerificationView
)

from dj_rest_auth.jwt_auth import get_refresh_view

# TokenObtainPairView, TokenRefreshView, TokenVerifyView, LoginView, LogoutView, PasswordChangeView, UserDetailsView, PasswordResetView, PasswordResetConfirmView, RegisterView, VerifyEmailView, ResendEmailVerificationView

# JWT Authentication views
TokenObtainPairView = TokenObtainPairView
TokenRefreshView = get_refresh_view
TokenVerifyView = TokenVerifyView

# Authentication views
LoginView = LoginView
LogoutView = LogoutView
PasswordChangeView = PasswordChangeView
PasswordResetView = PasswordResetView
PasswordResetConfirmView = PasswordResetConfirmView
UserDetailsView = UserDetailsView

# Registration views
RegisterView = RegisterView
VerifyEmailView = VerifyEmailView
ResendEmailVerificationView = ResendEmailVerificationView
