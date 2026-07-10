"""API views for behavioral anomaly detection."""

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.views import APIView

from ai_engines.behavioral_anomaly.services.engine import BehavioralAnomalyDetectionService
from apps.behavior.serializers import AnalyzeBehaviorSerializer
from core.permissions.roles import HasPlatformRole, PlatformRole
from core.responses import success_response


class AnalyzeBehaviorView(APIView):
    """Analyze user activity with the Behavioral Anomaly Detection Engine."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
    )

    @extend_schema(request=AnalyzeBehaviorSerializer)
    def post(self, request):
        serializer = AnalyzeBehaviorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant_id = serializer.validated_data.pop("tenant_id", "") or f"user-{request.user.id}"
        user_identifier = serializer.validated_data.pop("user_identifier")

        result = BehavioralAnomalyDetectionService().analyze(
            tenant_id=tenant_id,
            user_identifier=user_identifier,
            payload=serializer.validated_data,
        )
        return success_response(
            data=result,
            message="Behavioral anomaly analysis completed.",
            http_status=status.HTTP_200_OK,
        )
