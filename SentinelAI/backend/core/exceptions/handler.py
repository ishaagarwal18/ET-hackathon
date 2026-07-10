"""Custom DRF exception handling for standardized responses."""

from rest_framework.views import exception_handler


def _derive_message(detail):
    """Return an analyst-friendly message from DRF error details."""
    if isinstance(detail, dict):
        if "detail" in detail:
            return str(detail["detail"])
        first_key = next(iter(detail), None)
        if first_key:
            first_value = detail[first_key]
            if isinstance(first_value, list) and first_value:
                return f"{first_key}: {first_value[0]}"
            return f"{first_key}: {first_value}"
    if isinstance(detail, list) and detail:
        return str(detail[0])
    return "Request failed."


def sentinelai_exception_handler(exc, context):
    """Wrap DRF exceptions in the SentinelAI response envelope."""
    response = exception_handler(exc, context)
    if response is None:
        return response

    detail = response.data
    request = context.get("request") if context else None
    request_id = getattr(request, "request_id", None)

    response.data = {
        "success": False,
        "message": _derive_message(detail),
        "data": None,
        "errors": detail,
        "meta": {
            "status_code": response.status_code,
            "request_id": request_id,
        },
    }
    return response
