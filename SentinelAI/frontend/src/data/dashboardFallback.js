export const fallbackDashboard = {
  overview: {
    active_alerts: {
      total: 1284,
      by_severity: [
        { severity: "critical", count: 86 },
        { severity: "high", count: 231 },
        { severity: "medium", count: 604 },
        { severity: "low", count: 363 },
      ],
    },
    risk_score: {
      score: 72,
      level: "high",
      components: {
        asset_risk: 68,
        alert_pressure: 84,
        behavior_risk: 63,
        critical_assets: 942,
      },
    },
    assets: {
      total: 18642,
      by_type: [
        { label: "endpoint", count: 11200 },
        { label: "cloud", count: 3110 },
        { label: "identity", count: 1860 },
        { label: "network", count: 990 },
      ],
      highest_risk: [
        { asset_key: "AST-1044", name: "finance-workload-07", asset_type: "endpoint", risk_score: 94, criticality: "critical" },
        { asset_key: "AST-1181", name: "customer-data-vault", asset_type: "database", risk_score: 91, criticality: "critical" },
      ],
    },
    incidents: {
      active: 37,
      by_status: [
        { label: "triage", count: 11 },
        { label: "containment", count: 8 },
        { label: "eradication", count: 9 },
        { label: "recovery", count: 9 },
      ],
      recent: [
        { incident_key: "INC-2407", title: "Privileged account compromise", severity: "critical", status: "containment", priority: "p1", opened_at: "2026-07-05T08:10:00Z" },
        { incident_key: "INC-2399", title: "Endpoint malware investigation", severity: "high", status: "analysis", priority: "p2", opened_at: "2026-07-05T07:35:00Z" },
        { incident_key: "INC-2384", title: "Cloud policy drift exposure", severity: "medium", status: "eradication", priority: "p3", opened_at: "2026-07-05T06:25:00Z" },
      ],
    },
  },
  vulnerabilities: [
    { cve_id: "CVE-2026-11842", title: "Remote code execution in exposed gateway", severity: "critical", priority_score: 19.2 },
    { cve_id: "CVE-2026-10991", title: "Privilege escalation in endpoint agent", severity: "high", priority_score: 16.7 },
    { cve_id: "CVE-2025-8840", title: "Authentication bypass in admin console", severity: "critical", priority_score: 15.9 },
  ],
  logs: [
    { event_id: "EVT-901", source: "windows", event_type: "4625", severity: "high", message: "Multiple failed logon attempts", observed_at: "2026-07-05T08:52:00Z" },
    { event_id: "EVT-902", source: "firewall", event_type: "firewall_traffic", severity: "medium", message: "Blocked inbound SSH", observed_at: "2026-07-05T08:48:00Z" },
    { event_id: "EVT-903", source: "linux", event_type: "linux_auth", severity: "high", message: "Invalid SSH user from external IP", observed_at: "2026-07-05T08:44:00Z" },
  ],
  timeline: [
    { timestamp: "2026-07-05T00:00:00Z", severity: "medium", count: 32 },
    { timestamp: "2026-07-05T04:00:00Z", severity: "high", count: 44 },
    { timestamp: "2026-07-05T08:00:00Z", severity: "critical", count: 18 },
    { timestamp: "2026-07-05T12:00:00Z", severity: "medium", count: 57 },
    { timestamp: "2026-07-05T16:00:00Z", severity: "high", count: 49 },
    { timestamp: "2026-07-05T20:00:00Z", severity: "critical", count: 23 },
  ],
  threatMap: {
    indicators: [
      { indicator: "203.0.113.45", indicator_type: "ip", source: "CERT-In", severity: "critical", confidence: 94 },
      { indicator: "evil-update.example", indicator_type: "domain", source: "NVD enrichment", severity: "high", confidence: 87 },
      { indicator: "T1078", indicator_type: "ttp", source: "MITRE ATT&CK", severity: "high", confidence: 91 },
    ],
    by_type: [
      { label: "ip", count: 34 },
      { label: "domain", count: 21 },
      { label: "hash", count: 19 },
      { label: "ttp", count: 11 },
    ],
  },
};
