# django_app/modules/v1/users/urls.py

from rest_framework.routers import DefaultRouter
from .api import UsersViewSet

router = DefaultRouter()
router.register(r'', UsersViewSet, basename='users')

urlpatterns = router.urls
