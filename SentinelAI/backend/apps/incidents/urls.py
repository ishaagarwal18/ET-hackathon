"""URL routes for incidents."""

from django.urls import path

from apps.incidents.views import AutonomousIncidentResponseView


app_name = "incidents"

urlpatterns = [
    path("respond/", AutonomousIncidentResponseView.as_view(), name="autonomous-response"),
]
