from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core import views

app_name = 'core'

routers = DefaultRouter()
routers.register(
    'health-check', views.HealthCheckViewSet, basename='core_health_check'
)


urlpatterns = [path('', include(routers.urls))]
