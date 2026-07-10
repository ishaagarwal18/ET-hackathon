"""Shared pytest fixtures for SentinelAI tests."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.testing")


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def soc_user(db):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return User.objects.create_user(
        username="soc.analyst",
        email="soc.analyst@sentinelai.test",
        password="Str0ng-Test-Passphrase!",
        first_name="SOC",
        last_name="Analyst",
        role=User.Role.SOC_ANALYST,
        is_verified=True,
    )


@pytest.fixture
def auditor_user(db):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return User.objects.create_user(
        username="readonly.auditor",
        email="readonly.auditor@sentinelai.test",
        password="Str0ng-Test-Passphrase!",
        role=User.Role.READ_ONLY_AUDITOR,
        is_verified=True,
    )


@pytest.fixture
def authenticated_client(api_client, soc_user):
    api_client.force_authenticate(user=soc_user)
    return api_client


@pytest.fixture
def auditor_client(api_client, auditor_user):
    api_client.force_authenticate(user=auditor_user)
    return api_client


@pytest.fixture
def load_mock_data():
    def _load(name: str) -> dict:
        path = PROJECT_ROOT / "tests" / "mock_data" / name
        return json.loads(path.read_text(encoding="utf-8"))

    return _load
