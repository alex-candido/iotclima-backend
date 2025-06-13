# django_app/routes.py

from django.urls import include, path

urlpatterns = [
    path('auth/', include('django_app.modules.v1.auth.urls')),
]