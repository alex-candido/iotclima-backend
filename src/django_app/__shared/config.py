# django_app/__shared/config.py

from typing import Any, Dict, List, Literal, Tuple

import dj_database_url
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigService(BaseSettings):
    model_config = SettingsConfigDict(env_file="envs/.env", case_sensitive=True, extra="ignore")

    # Django Core Settings
    DEBUG: bool = True
    SECRET_KEY: str = ""
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Environment Settings
    ENVIRONMENT: Literal["development", "production", "test"] = "development"
    
    # Database Settings
    DATABASE_URL: str = ""
    
    @property
    def DATABASE_CONFIG(self) -> dj_database_url.DBConfig:
        if self.ENVIRONMENT.lower() == "development":
            return dj_database_url.parse(self.DATABASE_URL)
        if self.ENVIRONMENT.lower() == "production" and self.DATABASE_URL:
            return dj_database_url.parse(self.DATABASE_URL)
        if self.ENVIRONMENT.lower() == "test":
            return dj_database_url.parse("sqlite:///test_db.sqlite3")
        raise ValueError(f"DATABASE_URL must be set for production environment or invalid ENVIRONMENT: {self.ENVIRONMENT}.")
    
    # JWT Settings (Consider using Django's SECRET_KEY for JWT_SECRET_KEY if consistent)
    JWT_SECRET_KEY: str = 'django-insecure-0^ni+7nh3#9*clw*1%*s9_=b1-9$+hq@jh+b+ba(mg8m)cn+x'
    JWT_ACCESS_TOKEN_LIFETIME_MINUTES: int = 5
    JWT_REFRESH_TOKEN_LIFETIME_DAYS: int = 1
    JWT_ALGORITHM: str = "HS256"
    
    # CORS Settings
    CORS_ALLOW_ALL_ORIGINS: bool = False 
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000"
    ]
    
    # Email Settings
    EMAIL_BACKEND: str = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST: str = "smtp-relay.sendinblue.com"
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = True
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    DEFAULT_FROM_EMAIL: str = "alex.candido.tec@gmail.com"
    
    # Frontend URL (centralized and used for all redirects)
    FRONTEND_URL: str = "http://localhost:3000"
    
    LOGIN_URL: str = "/auth/sign-in"
    LOGIN_REDIRECT_URL: str = "/app"
    LOGOUT_REDIRECT_URL: str = "/"
    RESET_PASSWORD_REDIRECT_URL: str = "/auth/reset-password"
    
    # django-allauth (Config) [https://docs.allauth.org/en/dev/account/configuration.html]
    # django-allauth (signup) 
    ACCOUNT_SIGNUP_FIELDS: List[str] = ['email*', 'username*', 'password1*', 'password2*'] 
    
    # django-allauth (Login)
    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION: bool = False
    
    # django-allauth (Password Reset)
    ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED: bool = False
    
    # django-allauth (Email Verification)
    ACCOUNT_CONFIRM_EMAIL_ON_GET: bool = True
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS: int = 3
    ACCOUNT_EMAIL_VERIFICATION: str = 'mandatory'
    
    # django-allauth (Routing)
    ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS: bool = True
    ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL: str = LOGIN_URL
    ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL: str = LOGIN_REDIRECT_URL
    ACCOUNT_LOGOUT_REDIRECT_URL: str = LOGOUT_REDIRECT_URL 
    ACCOUNT_SIGNUP_REDIRECT_URL: str = LOGIN_REDIRECT_URL
    
    # django-allauth (Sending Email)
    ACCOUNT_EMAIL_SUBJECT_PREFIX: str = '[MyProject] '
    ACCOUNT_EMAIL_NOTIFICATIONS: bool = True
        
    # django-allauth (Email Addresses)
    ACCOUNT_UNIQUE_EMAIL: bool = True
    
    # dj-rest-auth settings [https://dj-rest-auth.readthedocs.io/en/latest/configuration.html?highlight=use_jwt]
    REST_AUTH_USE_JWT: bool = True
    REST_AUTH_PASSWORD_RESET_USE_SITES_DOMAIN: bool = False
    REST_AUTH_PASSWORD_RESET_SERIALIZER: str = 'django_app.modules.v1.auth.serializers.CustomPasswordResetSerializer'
    
    # django-rest-framework-simplejwt Settings [https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html]
    SIMPLE_JWT_ROTATE_REFRESH_TOKENS: bool = True 
    SIMPLE_JWT_BLACKLIST_AFTER_ROTATION: bool = True 
    SIMPLE_JWT_UPDATE_LAST_LOGIN: bool = False
    SIMPLE_JWT_AUTH_HEADER_TYPES: Tuple[str, ...] = ("Bearer",) 
    SIMPLE_JWT_AUTH_HEADER_NAME: str = "HTTP_AUTHORIZATION"
    SIMPLE_JWT_USER_ID_FIELD: str = "id" 
    SIMPLE_JWT_USER_ID_CLAIM: str = "user_id" 
    SIMPLE_JWT_TOKEN_TYPE_CLAIM: str = "token_type" 
    SIMPLE_JWT_JTI_CLAIM: str = "jti" 
    
    # Authentication Backends  
    AUTHENTICATION_BACKENDS_LIST: Tuple[str, ...] = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    )
    