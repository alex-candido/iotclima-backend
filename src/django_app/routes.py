# django_app/routes.py

from django.urls import include, path

urlpatterns = [
    path('places/', include('django_app.modules.v1.places.urls')),
    path('users/', include('django_app.modules.v1.users.urls')),
    path('auth/', include('django_app.modules.v1.auth.urls')),
]