"""API views for the Threat Intelligence Agent."""

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.views import APIView

from agents.threat_intelligence.services.chat_service import ThreatIntelligenceChatService
from apps.threat_intelligence.serializers import ThreatIntelChatSerializer, ThreatIntelHistorySerializer
from core.permissions.roles import HasPlatformRole, PlatformRole
from core.responses import error_response, success_response


class TenantMixin:
    """Resolve tenant context until organization tenancy is fully implemented."""

    def resolve_tenant_id(self, request, serializer):
        tenant_id = serializer.validated_data.get("tenant_id")
        return tenant_id or f"user-{request.user.id}"


class ThreatIntelChatView(TenantMixin, APIView):
    """Answer threat intelligence questions using RAG."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
        PlatformRole.READ_ONLY_AUDITOR,
    )

    @extend_schema(request=ThreatIntelChatSerializer)
    def post(self, request):
        serializer = ThreatIntelChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = ThreatIntelligenceChatService().chat(
                tenant_id=self.resolve_tenant_id(request, serializer),
                user_id=str(request.user.id),
                question=serializer.validated_data["question"],
                top_k=serializer.validated_data["top_k"],
            )
        except RuntimeError as exc:
            return error_response(message=str(exc), http_status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return success_response(data=result, message="Threat intelligence answer generated.")


class ThreatIntelChatHistoryView(TenantMixin, APIView):
    """Return threat intelligence chat history."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
        PlatformRole.READ_ONLY_AUDITOR,
    )

    @extend_schema(parameters=[ThreatIntelHistorySerializer])
    def get(self, request):
        serializer = ThreatIntelHistorySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        history = ThreatIntelligenceChatService().history(
            tenant_id=self.resolve_tenant_id(request, serializer),
            user_id=str(request.user.id),
            limit=serializer.validated_data["limit"],
            offset=serializer.validated_data["offset"],
        )
        return success_response(data=history, message="Threat intelligence chat history loaded.")
