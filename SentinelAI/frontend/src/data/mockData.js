export const kpis = [
  { label: "Open Alerts", value: "1,284", change: "+12.5%", tone: "red" },
  { label: "Active Incidents", value: "37", change: "-8.2%", tone: "amber" },
  { label: "Protected Assets", value: "18.6K", change: "+4.1%", tone: "green" },
  { label: "Risk Score", value: "72", change: "+6 pts", tone: "blue" },
];

export const alertVolume = {
  labels: ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
  datasets: [
    {
      label: "Alerts",
      data: [320, 460, 390, 710, 640, 820],
      borderColor: "#2563eb",
      backgroundColor: "rgba(37, 99, 235, 0.14)",
      fill: true,
      tension: 0.42,
    },
    {
      label: "Confirmed Threats",
      data: [42, 58, 73, 120, 96, 132],
      borderColor: "#ef4444",
      backgroundColor: "rgba(239, 68, 68, 0.08)",
      fill: true,
      tension: 0.42,
    },
  ],
};

export const riskBreakdown = {
  labels: ["Identity", "Endpoint", "Cloud", "Network", "Application"],
  datasets: [
    {
      data: [28, 22, 24, 16, 10],
      backgroundColor: ["#2563eb", "#06b6d4", "#f59e0b", "#ef4444", "#10b981"],
      borderWidth: 0,
    },
  ],
};

export const attackEvents = [
  { time: "09:15", title: "Suspicious identity provider login", severity: "High", source: "Identity" },
  { time: "10:40", title: "Endpoint command anomaly observed", severity: "Medium", source: "EDR" },
  { time: "11:25", title: "Lateral movement pattern detected", severity: "Critical", source: "Network" },
  { time: "13:05", title: "Privilege escalation signal correlated", severity: "High", source: "SIEM" },
];

export const threatNodes = [
  { id: "Credential Theft", x: 50, y: 44, level: "critical" },
  { id: "Cloud IAM", x: 27, y: 22, level: "high" },
  { id: "Endpoint Cluster", x: 72, y: 27, level: "medium" },
  { id: "Data Store", x: 34, y: 72, level: "high" },
  { id: "Ticketing", x: 76, y: 72, level: "low" },
];

export const alertRows = [
  ["ALT-9012", "Credential spray threshold exceeded", "Critical", "Identity", "Open"],
  ["ALT-8998", "Impossible travel pattern", "High", "Cloud", "Triaged"],
  ["ALT-8977", "Unsigned PowerShell execution", "Medium", "Endpoint", "Open"],
  ["ALT-8920", "Data exfiltration volume anomaly", "High", "Network", "Investigating"],
];

export const incidentRows = [
  ["INC-2407", "Privileged account compromise", "Critical", "Containment", "Alex Morgan"],
  ["INC-2399", "Endpoint malware investigation", "High", "Analysis", "Riya Shah"],
  ["INC-2384", "Cloud policy drift exposure", "Medium", "Eradication", "Noah Kim"],
];

export const assetRows = [
  ["AST-1009", "prod-auth-gateway", "Cloud", "Critical", "Healthy"],
  ["AST-1044", "finance-workload-07", "Endpoint", "High", "At Risk"],
  ["AST-1181", "customer-data-vault", "Database", "Critical", "Monitored"],
  ["AST-1220", "edge-fw-us-east", "Network", "High", "Healthy"],
];
