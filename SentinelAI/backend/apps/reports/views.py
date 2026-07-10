"""API views for reports."""

from django.http import FileResponse
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.views import APIView

from apps.reports.serializers import IncidentReportSerializer
from apps.reports.services.report_service import IncidentReportService
from core.permissions.roles import HasPlatformRole, PlatformRole
from core.responses import error_response, success_response


class GenerateIncidentReportView(APIView):
    """Generate downloadable incident report files."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
        PlatformRole.READ_ONLY_AUDITOR,
    )

    @extend_schema(request=IncidentReportSerializer)
    def post(self, request):
        serializer = IncidentReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = dict(serializer.validated_data)
        formats = payload.pop("formats")
        tenant_id = payload.pop("tenant_id", "") or f"user-{request.user.id}"

        try:
            result = IncidentReportService().generate(
                tenant_id=tenant_id,
                requested_by=str(request.user.id),
                payload=payload,
                formats=formats,
            )
        except RuntimeError as exc:
            return error_response(message=str(exc), http_status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return success_response(data=result, message="Incident report generated.", http_status=status.HTTP_201_CREATED)


class DownloadReportView(APIView):
    """Download a generated report file."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
        PlatformRole.READ_ONLY_AUDITOR,
    )

    def get(self, request, filename: str):
        try:
            path, content_type = IncidentReportService().resolve_download(filename)
        except ValueError as exc:
            return error_response(message=str(exc), http_status=status.HTTP_400_BAD_REQUEST)
        except FileNotFoundError as exc:
            return error_response(message=str(exc), http_status=status.HTTP_404_NOT_FOUND)

        return FileResponse(path.open("rb"), as_attachment=True, filename=path.name, content_type=content_type)
