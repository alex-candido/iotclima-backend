# django_app/modules/v1/logs/urls.py

from rest_framework.routers import DefaultRouter
from .api import LogsViewSet

router = DefaultRouter()
router.register(r'', LogsViewSet, basename='logs')

urlpatterns = router.urls
