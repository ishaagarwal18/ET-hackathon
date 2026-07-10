"""API views for logs."""

from bson.errors import InvalidId
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.views import APIView

from agents.log_collector.services.collector import LogCollectorService
from apps.logs.serializers import ListLogsSerializer, LogDetailsSerializer, UploadLogSerializer
from core.permissions.roles import HasPlatformRole, PlatformRole
from core.responses import error_response, success_response


class TenantResolutionMixin:
    """Resolve tenant context until organization tenancy is implemented."""

    def resolve_tenant_id(self, request, serializer):
        tenant_id = serializer.validated_data.get("tenant_id")
        if tenant_id:
            return tenant_id
        return f"user-{request.user.id}"


class UploadLogView(TenantResolutionMixin, APIView):
    """Upload, normalize, and store logs using Agent 1."""

    parser_classes = (JSONParser, MultiPartParser, FormParser)
    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
    )

    @extend_schema(request=UploadLogSerializer)
    def post(self, request):
        serializer = UploadLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data.get("file")
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8", errors="replace")
        else:
            content = serializer.validated_data["content"]

        result = LogCollectorService().ingest(
            tenant_id=self.resolve_tenant_id(request, serializer),
            source_type=serializer.validated_data["source_type"],
            source_name=serializer.validated_data.get("source_name"),
            content=content,
        )
        return success_response(data=result, message="Logs normalized and stored.", http_status=status.HTTP_201_CREATED)


class ListLogsView(TenantResolutionMixin, APIView):
    """List normalized logs."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
        PlatformRole.READ_ONLY_AUDITOR,
    )

    @extend_schema(parameters=[ListLogsSerializer])
    def get(self, request):
        serializer = ListLogsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        filters = {}
        for field in ("source_type", "severity", "status"):
            if serializer.validated_data.get(field):
                filters[field] = serializer.validated_data[field]

        result = LogCollectorService().list_logs(
            tenant_id=self.resolve_tenant_id(request, serializer),
            limit=serializer.validated_data["limit"],
            offset=serializer.validated_data["offset"],
            filters=filters,
        )
        return success_response(data=result["items"], message="Logs loaded.", meta=result["pagination"])


class LogDetailsView(TenantResolutionMixin, APIView):
    """Return one normalized log document."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
        PlatformRole.READ_ONLY_AUDITOR,
    )

    @extend_schema(parameters=[LogDetailsSerializer])
    def get(self, request):
        serializer = LogDetailsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        try:
            log = LogCollectorService().get_log_details(
                tenant_id=self.resolve_tenant_id(request, serializer),
                log_id=serializer.validated_data["log_id"],
            )
        except InvalidId:
            return error_response(message="Invalid log ID.", http_status=status.HTTP_400_BAD_REQUEST)

        if not log:
            return error_response(message="Log not found.", http_status=status.HTTP_404_NOT_FOUND)

        return success_response(data=log, message="Log details loaded.")
