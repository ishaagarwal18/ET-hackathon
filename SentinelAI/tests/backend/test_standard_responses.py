"""Unit tests for standardized API response helpers."""

import pytest
from rest_framework import status

from core.responses import error_response, success_response


pytestmark = pytest.mark.unit


def test_success_response_contract():
    response = success_response(data={"id": "alert-1"}, message="Loaded.", meta={"total": 1})

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "success": True,
        "message": "Loaded.",
        "data": {"id": "alert-1"},
        "errors": None,
        "meta": {"total": 1},
    }


def test_error_response_contract():
    response = error_response(message="Invalid.", errors={"field": ["required"]})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["success"] is False
    assert response.data["data"] is None
    assert response.data["errors"] == {"field": ["required"]}
