"""Authentication and security context middleware."""

import logging
import time
import uuid


security_logger = logging.getLogger("sentinelai.security")


class SecurityContextMiddleware:
    """Attach request IDs and emit security-relevant authentication events."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        started_at = time.perf_counter()
        response = self.get_response(request)
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        response["X-Request-ID"] = request.request_id
        response["X-Response-Time-ms"] = str(duration_ms)

        user = getattr(request, "user", None)
        if request.path.startswith("/api/"):
            user_id = getattr(user, "id", None) if user and user.is_authenticated else "anonymous"
            role = getattr(user, "role", "anonymous") if user and user.is_authenticated else "anonymous"
            security_logger.info(
                "api_request path=%s method=%s status=%s duration_ms=%s user_id=%s role=%s request_id=%s",
                request.path,
                request.method,
                response.status_code,
                duration_ms,
                user_id,
                role,
                request.request_id,
            )

        return response
