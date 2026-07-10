import { apiClient, unwrapApiResponse } from "./apiClient.js";

const dashboardEndpoints = {
  overview: "/dashboard/overview/",
  activeAlerts: "/dashboard/active-alerts/",
  riskScore: "/dashboard/risk-score/",
  assets: "/dashboard/assets/",
  incidents: "/dashboard/incidents/",
  topVulnerabilities: "/dashboard/top-vulnerabilities/",
  recentLogs: "/dashboard/recent-logs/",
  attackTimeline: "/dashboard/attack-timeline/",
  threatMap: "/dashboard/threat-map/",
};

export async function fetchDashboardSnapshot() {
  const [overview, vulnerabilities, logs, timeline, threatMap] = await Promise.all([
    apiClient.get(dashboardEndpoints.overview).then(unwrapApiResponse),
    apiClient.get(dashboardEndpoints.topVulnerabilities, { params: { limit: 8 } }).then(unwrapApiResponse),
    apiClient.get(dashboardEndpoints.recentLogs, { params: { limit: 12 } }).then(unwrapApiResponse),
    apiClient.get(dashboardEndpoints.attackTimeline, { params: { hours: 24 } }).then(unwrapApiResponse),
    apiClient.get(dashboardEndpoints.threatMap, { params: { limit: 20 } }).then(unwrapApiResponse),
  ]);

  return {
    overview,
    vulnerabilities,
    logs,
    timeline,
    threatMap,
  };
}
