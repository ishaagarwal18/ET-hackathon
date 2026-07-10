"""URL routes for dashboard."""

from django.urls import path

from apps.dashboard.views import (
    ActiveAlertsView,
    AssetsSummaryView,
    AttackTimelineView,
    DashboardOverviewView,
    IncidentsSummaryView,
    RecentLogsView,
    RiskScoreView,
    ThreatMapView,
    TopVulnerabilitiesView,
)


app_name = "dashboard"

urlpatterns = [
    path("overview/", DashboardOverviewView.as_view(), name="overview"),
    path("active-alerts/", ActiveAlertsView.as_view(), name="active-alerts"),
    path("risk-score/", RiskScoreView.as_view(), name="risk-score"),
    path("assets/", AssetsSummaryView.as_view(), name="assets-summary"),
    path("incidents/", IncidentsSummaryView.as_view(), name="incidents-summary"),
    path("top-vulnerabilities/", TopVulnerabilitiesView.as_view(), name="top-vulnerabilities"),
    path("recent-logs/", RecentLogsView.as_view(), name="recent-logs"),
    path("attack-timeline/", AttackTimelineView.as_view(), name="attack-timeline"),
    path("threat-map/", ThreatMapView.as_view(), name="threat-map"),
]
