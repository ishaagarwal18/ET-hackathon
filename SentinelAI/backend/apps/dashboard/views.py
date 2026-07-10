"""API views for dashboard."""

from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.views import APIView

from apps.dashboard.serializers import DashboardLimitSerializer, DashboardTenantSerializer, DashboardTimelineSerializer
from apps.dashboard.services.dashboard_service import DashboardService
from core.permissions.roles import HasPlatformRole, PlatformRole
from core.responses import success_response


class DashboardTenantMixin:
    """Resolve tenant context for dashboard aggregation."""

    def resolve_tenant_id(self, request, serializer):
        tenant_id = serializer.validated_data.get("tenant_id")
        return tenant_id or f"user-{request.user.id}"


class DashboardBaseView(DashboardTenantMixin, APIView):
    """Base dashboard API view."""

    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SOC_ANALYST,
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
        PlatformRole.READ_ONLY_AUDITOR,
    )
    service_class = DashboardService


class DashboardOverviewView(DashboardBaseView):
    """Return primary dashboard cards."""

    @extend_schema(parameters=[DashboardTenantSerializer])
    def get(self, request):
        serializer = DashboardTenantSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = self.service_class().overview(tenant_id=self.resolve_tenant_id(request, serializer))
        return success_response(data=data, message="Dashboard overview loaded.")


class ActiveAlertsView(DashboardBaseView):
    """Return active alerts card data."""

    @extend_schema(parameters=[DashboardTenantSerializer])
    def get(self, request):
        serializer = DashboardTenantSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = self.service_class().repository.active_alerts(tenant_id=self.resolve_tenant_id(request, serializer))
        return success_response(data=data, message="Active alerts loaded.")


class RiskScoreView(DashboardBaseView):
    """Return aggregate risk score card data."""

    @extend_schema(parameters=[DashboardTenantSerializer])
    def get(self, request):
        serializer = DashboardTenantSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = self.service_class().repository.risk_score(tenant_id=self.resolve_tenant_id(request, serializer))
        return success_response(data=data, message="Risk score loaded.")


class AssetsSummaryView(DashboardBaseView):
    """Return assets dashboard data."""

    @extend_schema(parameters=[DashboardTenantSerializer])
    def get(self, request):
        serializer = DashboardTenantSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = self.service_class().repository.assets(tenant_id=self.resolve_tenant_id(request, serializer))
        return success_response(data=data, message="Assets summary loaded.")


class IncidentsSummaryView(DashboardBaseView):
    """Return incidents dashboard data."""

    @extend_schema(parameters=[DashboardTenantSerializer])
    def get(self, request):
        serializer = DashboardTenantSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = self.service_class().repository.incidents(tenant_id=self.resolve_tenant_id(request, serializer))
        return success_response(data=data, message="Incidents summary loaded.")


class TopVulnerabilitiesView(DashboardBaseView):
    """Return top vulnerabilities."""

    @extend_schema(parameters=[DashboardLimitSerializer])
    def get(self, request):
        serializer = DashboardLimitSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = self.service_class().top_vulnerabilities(
            tenant_id=self.resolve_tenant_id(request, serializer),
            limit=serializer.validated_data["limit"],
        )
        return success_response(data=data, message="Top vulnerabilities loaded.")


class RecentLogsView(DashboardBaseView):
    """Return recent logs."""

    @extend_schema(parameters=[DashboardLimitSerializer])
    def get(self, request):
        serializer = DashboardLimitSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = self.service_class().recent_logs(
            tenant_id=self.resolve_tenant_id(request, serializer),
            limit=serializer.validated_data["limit"],
        )
        return success_response(data=data, message="Recent logs loaded.")


class AttackTimelineView(DashboardBaseView):
    """Return attack timeline data."""

    @extend_schema(parameters=[DashboardTimelineSerializer])
    def get(self, request):
        serializer = DashboardTimelineSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = self.service_class().attack_timeline(
            tenant_id=self.resolve_tenant_id(request, serializer),
            hours=serializer.validated_data["hours"],
        )
        return success_response(data=data, message="Attack timeline loaded.")


class ThreatMapView(DashboardBaseView):
    """Return threat map data."""

    @extend_schema(parameters=[DashboardLimitSerializer])
    def get(self, request):
        serializer = DashboardLimitSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = self.service_class().threat_map(
            tenant_id=self.resolve_tenant_id(request, serializer),
            limit=serializer.validated_data["limit"],
        )
        return success_response(data=data, message="Threat map loaded.")
