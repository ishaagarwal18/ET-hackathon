"""API tests for Agent 1 log collector endpoints."""

from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from bson import ObjectId
from django.urls import reverse
from rest_framework import status


pytestmark = pytest.mark.api


class FakeLogCollectorService:
    logs = [
        {
            "id": str(ObjectId()),
            "tenant_id": "tenant-red",
            "source_type": "json",
            "severity": "high",
            "message": "Privilege escalation attempt",
            "observed_at": datetime(2026, 7, 6, 10, 15, tzinfo=UTC).isoformat(),
            "deleted_at": None,
        }
    ]

    def ingest(self, **kwargs):
        return {
            "source_type": kwargs["source_type"],
            "source_name": kwargs.get("source_name") or kwargs["source_type"],
            "received": 1,
            "stored": 1,
            "log_ids": [self.logs[0]["id"]],
        }

    def list_logs(self, **kwargs):
        return {"items": self.logs, "pagination": {"limit": kwargs["limit"], "offset": kwargs["offset"], "total": 1}}

    def get_log_details(self, **kwargs):
        return self.logs[0] if kwargs["log_id"] == self.logs[0]["id"] else None


@patch("apps.logs.views.LogCollectorService", FakeLogCollectorService)
def test_upload_log_normalizes_and_returns_inserted_ids(authenticated_client, load_mock_data):
    payload = load_mock_data("log_json_payload.json")

    response = authenticated_client.post(reverse("logs:upload-log"), payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"] is True
    assert response.data["data"]["stored"] == 1
    assert response.data["data"]["source_type"] == "json"


@patch("apps.logs.views.LogCollectorService", FakeLogCollectorService)
def test_list_logs_returns_pagination_metadata(authenticated_client):
    response = authenticated_client.get(reverse("logs:list-logs"), {"tenant_id": "tenant-red", "limit": 10})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["data"][0]["message"] == "Privilege escalation attempt"
    assert response.data["meta"]["total"] == 1


@patch("apps.logs.views.LogCollectorService", FakeLogCollectorService)
def test_log_details_handles_missing_log(authenticated_client):
    response = authenticated_client.get(
        reverse("logs:log-details"),
        {"tenant_id": "tenant-red", "log_id": "000000000000000000000000"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["success"] is False
