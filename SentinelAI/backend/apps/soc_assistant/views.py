"""API views for the AI SOC Assistant."""

from django.http import StreamingHttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.views import APIView

from agents.soc_assistant.services.assistant_service import SOCAssistantService
from apps.soc_assistant.serializers import SOCAssistantChatSerializer, SOCAssistantHistorySerializer
from core.permissions.roles import HasPlatformRole, PlatformRole
from core.responses import error_response, success_response


class SOCAssistantTenantMixin:
    """Resolve tenant context until organization tenancy is fully implemented."""

    def resolve_tenant_id(self, request, serializer):
        tenant_id = serializer.validated_data.get("tenant_id")
        return tenant_id or f"user-{request.user.id}"


class SOCAssistantBaseView(SOCAssistantTenantMixin, APIView):
    """Base SOC Assistant API view."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
        PlatformRole.READ_ONLY_AUDITOR,
    )


class SOCAssistantChatView(SOCAssistantBaseView):
    """Return a complete SOC Assistant response."""

    @extend_schema(request=SOCAssistantChatSerializer)
    def post(self, request):
        serializer = SOCAssistantChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = SOCAssistantService().chat(
                tenant_id=self.resolve_tenant_id(request, serializer),
                user_id=str(request.user.id),
                message=serializer.validated_data["message"],
                context=serializer.validated_data.get("context", {}),
            )
        except RuntimeError as exc:
            return error_response(message=str(exc), http_status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return success_response(data=result, message="SOC Assistant response generated.")


class SOCAssistantStreamView(SOCAssistantBaseView):
    """Stream a SOC Assistant response using server-sent events."""

    @extend_schema(request=SOCAssistantChatSerializer)
    def post(self, request):
        serializer = SOCAssistantChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = SOCAssistantService()
        try:
            result = service.chat(
                tenant_id=self.resolve_tenant_id(request, serializer),
                user_id=str(request.user.id),
                message=serializer.validated_data["message"],
                context=serializer.validated_data.get("context", {}),
            )
        except RuntimeError as exc:
            return error_response(message=str(exc), http_status=status.HTTP_503_SERVICE_UNAVAILABLE)

        response = StreamingHttpResponse(
            service.stream_events(response=result),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response


class SOCAssistantHistoryView(SOCAssistantBaseView):
    """Return SOC Assistant conversation history."""

    @extend_schema(parameters=[SOCAssistantHistorySerializer])
    def get(self, request):
        serializer = SOCAssistantHistorySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        history = SOCAssistantService().history(
            tenant_id=self.resolve_tenant_id(request, serializer),
            user_id=str(request.user.id),
            limit=serializer.validated_data["limit"],
            offset=serializer.validated_data["offset"],
        )
        return success_response(data=history, message="SOC Assistant history loaded.")
