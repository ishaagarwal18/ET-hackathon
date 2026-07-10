"""URL routes for AI Attack Prediction Agent APIs."""

from django.urls import path

from apps.attack_prediction.views import AttackPredictionView


app_name = "attack_prediction"

urlpatterns = [
    path("predict/", AttackPredictionView.as_view(), name="predict"),
]
