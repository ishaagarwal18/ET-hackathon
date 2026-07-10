"""API views for incidents."""

from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.views import APIView

from agents.incident_response.services.response_service import AutonomousIncidentResponseService
from apps.incidents.serializers import AutonomousIncidentResponseSerializer
from core.permissions.roles import HasPlatformRole, PlatformRole
from core.responses import success_response


class AutonomousIncidentResponseView(APIView):
    """Simulate autonomous incident response playbook execution."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
    )

    @extend_schema(request=AutonomousIncidentResponseSerializer)
    def post(self, request):
        serializer = AutonomousIncidentResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AutonomousIncidentResponseService().respond(**serializer.validated_data)
        return success_response(data=result, message="Incident response simulation completed.")
