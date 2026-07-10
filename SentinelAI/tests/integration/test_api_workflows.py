"""Integration tests for authenticated SentinelAI API workflows."""

from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status


pytestmark = pytest.mark.integration


def test_authenticated_behavior_analysis_workflow(authenticated_client, load_mock_data):
    payload = load_mock_data("behavior_activity.json")
    expected = {
        "profile_id": "profile-test-001",
        "user_identifier": payload["user_identifier"],
        "risk_score": 92,
        "anomaly_score": 0.82,
        "confidence_score": 94,
        "is_anomaly": True,
        "explanation": ["High-risk activity detected."],
        "features": {"failed_login_count": 7.0},
    }

    with patch("apps.behavior.views.BehavioralAnomalyDetectionService") as service_cls:
        service_cls.return_value.analyze.return_value = expected
        response = authenticated_client.post(reverse("behavior:analyze"), payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"]["risk_score"] == 92
    service_cls.return_value.analyze.assert_called_once()


def test_read_only_auditor_cannot_trigger_behavior_analysis(auditor_client, load_mock_data):
    response = auditor_client.post(reverse("behavior:analyze"), load_mock_data("behavior_activity.json"), format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_attack_prediction_api_returns_standard_response(authenticated_client, load_mock_data):
    payload = load_mock_data("attack_prediction.json")

    response = authenticated_client.post(reverse("attack_prediction:predict"), payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["success"] is True
    assert response.data["data"]["predicted_stage"] == "discovery"


def test_incident_report_generation_api_uses_report_service(authenticated_client, load_mock_data):
    payload = load_mock_data("incident_report.json")
    expected = {
        "report_id": "RPT-001",
        "incident_id": payload["incident"]["incident_id"],
        "generated_at": "2026-07-06T10:30:00Z",
        "files": [{"format": "json", "filename": "incident.json"}],
        "report": {"incident": payload["incident"]},
    }

    with patch("apps.reports.views.IncidentReportService") as service_cls:
        service_cls.return_value.generate.return_value = expected
        response = authenticated_client.post(reverse("reports:generate-incident-report"), payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["data"]["report_id"] == "RPT-001"
    service_cls.return_value.generate.assert_called_once()
