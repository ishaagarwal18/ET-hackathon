"""API tests for secure authentication endpoints."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


pytestmark = [pytest.mark.api, pytest.mark.django_db]


def test_register_rejects_security_admin_self_service(api_client):
    url = reverse("authentication:register")

    response = api_client.post(
        url,
        {
            "username": "admin.request",
            "email": "admin.request@sentinelai.test",
            "first_name": "Admin",
            "last_name": "Request",
            "role": "security_admin",
            "password": "Str0ng-Test-Passphrase!",
            "password_confirm": "Str0ng-Test-Passphrase!",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["success"] is False


def test_register_and_login_issue_jwt_tokens(api_client):
    register_url = reverse("authentication:register")
    login_url = reverse("authentication:jwt-login")

    response = api_client.post(
        register_url,
        {
            "username": "new.analyst",
            "email": "new.analyst@sentinelai.test",
            "first_name": "New",
            "last_name": "Analyst",
            "role": "soc_analyst",
            "password": "Str0ng-Test-Passphrase!",
            "password_confirm": "Str0ng-Test-Passphrase!",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["success"] is True
    assert response.data["data"]["role"] == "soc_analyst"

    login = api_client.post(
        login_url,
        {"username": "new.analyst", "password": "Str0ng-Test-Passphrase!"},
        format="json",
    )

    assert login.status_code == status.HTTP_200_OK
    assert {"access", "refresh", "user"}.issubset(login.data["data"])
    assert login.data["data"]["user"]["email"] == "new.analyst@sentinelai.test"


def test_me_requires_authenticated_user(api_client, authenticated_client, soc_user):
    from rest_framework.test import APIClient

    url = reverse("authentication:me")

    unauthenticated = APIClient().get(url)
    authenticated = authenticated_client.get(url)

    assert unauthenticated.status_code == status.HTTP_401_UNAUTHORIZED
    assert authenticated.status_code == status.HTTP_200_OK
    assert authenticated.data["data"]["id"] == soc_user.id


def test_password_reset_request_is_account_enumeration_safe(api_client, soc_user, mailoutbox):
    url = reverse("authentication:password-reset-request")

    response = api_client.post(url, {"email": soc_user.email}, format="json")
    missing = api_client.post(url, {"email": "missing@sentinelai.test"}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert missing.status_code == status.HTTP_200_OK
    assert response.data["message"] == missing.data["message"]
    assert len(mailoutbox) == 1
    assert get_user_model().objects.filter(email=soc_user.email).exists()
