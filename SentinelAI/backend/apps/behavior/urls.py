"""URL routes for behavioral anomaly detection."""

from django.urls import path

from apps.behavior.views import AnalyzeBehaviorView


app_name = "behavior"

urlpatterns = [
    path("analyze/", AnalyzeBehaviorView.as_view(), name="analyze"),
]
