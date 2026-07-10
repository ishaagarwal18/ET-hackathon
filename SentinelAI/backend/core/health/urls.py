"""Health check URL routes."""

from django.urls import path

from core.health.views import HealthCheckView


app_name = "health"

urlpatterns = [
    path("", HealthCheckView.as_view(), name="health-check"),
]
