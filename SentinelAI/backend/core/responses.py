"""Standardized API response helpers."""

from typing import Any

from rest_framework import status
from rest_framework.response import Response


def success_response(
    data: Any = None,
    message: str = "Request completed successfully.",
    http_status: int = status.HTTP_200_OK,
    meta: dict | None = None,
) -> Response:
    """Return a consistent successful API response."""
    payload = {
        "success": True,
        "message": message,
        "data": data,
        "errors": None,
        "meta": meta or {},
    }
    return Response(payload, status=http_status)


def error_response(
    message: str = "Request failed.",
    errors: Any = None,
    http_status: int = status.HTTP_400_BAD_REQUEST,
    meta: dict | None = None,
) -> Response:
    """Return a consistent error API response."""
    payload = {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors,
        "meta": meta or {},
    }
    return Response(payload, status=http_status)
