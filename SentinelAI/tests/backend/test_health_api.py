"""API tests for platform health endpoint."""

import pytest
from django.urls import reverse
from rest_framework import status


pytestmark = pytest.mark.api


def test_health_check_reports_healthy_mongodb(api_client, monkeypatch):
    monkeypatch.setattr("core.health.views.check_mongodb_connection", lambda: True)

    response = api_client.get(reverse("health:health-check"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "healthy"
    assert response.data["dependencies"]["mongodb"] == "healthy"


def test_health_check_reports_degraded_mongodb(api_client, monkeypatch):
    def fail_ping():
        raise RuntimeError("mongo unavailable")

    monkeypatch.setattr("core.health.views.check_mongodb_connection", fail_ping)

    response = api_client.get(reverse("health:health-check"))

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.data["status"] == "degraded"
    assert response.data["dependencies"]["mongodb"] == "unhealthy"
