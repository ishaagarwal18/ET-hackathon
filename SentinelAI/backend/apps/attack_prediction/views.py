"""API views for the AI Attack Prediction Agent."""

from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.views import APIView

from agents.attack_prediction.services.predictor import AttackPredictionService
from apps.attack_prediction.serializers import AttackPredictionSerializer
from core.permissions.roles import HasPlatformRole, PlatformRole
from core.responses import success_response


class AttackPredictionView(APIView):
    """Predict likely next attacker action."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
    )

    @extend_schema(request=AttackPredictionSerializer)
    def post(self, request):
        serializer = AttackPredictionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AttackPredictionService().predict(**serializer.validated_data)
        return success_response(data=result, message="Attack prediction completed.")
