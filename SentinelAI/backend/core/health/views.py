"""Health check API views."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.health.serializers import HealthCheckSerializer
from core.mongodb import check_mongodb_connection


class HealthCheckView(APIView):
    """Expose platform liveness and dependency status."""

    authentication_classes = ()
    permission_classes = (AllowAny,)

    @extend_schema(responses=HealthCheckSerializer)
    def get(self, request):
        dependencies = {"mongodb": "healthy"}
        response_status = status.HTTP_200_OK
        platform_status = "healthy"

        try:
            check_mongodb_connection()
        except Exception:
            dependencies["mongodb"] = "unhealthy"
            platform_status = "degraded"
            response_status = status.HTTP_503_SERVICE_UNAVAILABLE

        payload = {
            "status": platform_status,
            "service": "sentinelai-backend",
            "version": "1.0.0",
            "dependencies": dependencies,
        }
        return Response(payload, status=response_status)
