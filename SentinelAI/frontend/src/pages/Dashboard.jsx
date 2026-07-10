import { useEffect, useMemo, useState } from "react";
import { Bar, Line } from "react-chartjs-2";
import { AnimatePresence, motion } from "framer-motion";
import { AlertTriangle, Bot, Clock3, Database, Radar, Send, Server, ShieldAlert, Zap } from "lucide-react";

import Card from "../components/common/Card.jsx";
import { fallbackDashboard } from "../data/dashboardFallback.js";
import { fetchDashboardSnapshot } from "../services/dashboardApi.js";
import { sendThreatIntelQuestion } from "../services/threatIntelApi.js";
import { cn } from "../utils/cn.js";

const REFRESH_INTERVAL_MS = 10000;

function severityClass(severity) {
  const map = {
    critical: "bg-red-500/15 text-red-200 ring-red-400/30",
    high: "bg-amber-500/15 text-amber-200 ring-amber-400/30",
    medium: "bg-blue-500/15 text-blue-200 ring-blue-400/30",
    low: "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30",
  };
  return map[String(severity).toLowerCase()] || "bg-slate-500/15 text-slate-200 ring-slate-400/30";
}

function formatTime(value) {
  if (!value) return "n/a";
  return new Intl.DateTimeFormat("en", {
    hour: "2-digit",
    minute: "2-digit",
    month: "short",
    day: "2-digit",
  }).format(new Date(value));
}

function LiveMetricCard({ icon: Icon, label, value, detail, tone = "blue" }) {
  const tones = {
    red: "from-red-500/20 to-red-500/5 text-red-200",
    amber: "from-amber-500/20 to-amber-500/5 text-amber-200",
    blue: "from-blue-500/20 to-cyan-500/5 text-blue-200",
    emerald: "from-emerald-500/20 to-emerald-500/5 text-emerald-200",
  };

  return (
    <motion.div
      whileHover={{ y: -2 }}
      className="rounded-lg border border-white/10 bg-slate-950/70 p-4 shadow-2xl shadow-slate-950/30 backdrop-blur"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase text-slate-400">{label}</p>
          <p className="mt-3 text-3xl font-semibold text-white">{value}</p>
          <p className="mt-2 text-sm text-slate-400">{detail}</p>
        </div>
        <div className={cn("rounded-lg bg-gradient-to-br p-3 ring-1", tones[tone])}>
          <Icon size={21} />
        </div>
      </div>
    </motion.div>
  );
}

function ConnectedRiskMeter({ risk }) {
  const score = Number(risk?.score || 0);
  const radius = 68;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <Card className="border-white/10 bg-slate-950/70 text-white shadow-2xl shadow-slate-950/30" title="Risk Meter">
      <div className="flex flex-col items-center gap-5">
        <div className="relative h-44 w-44">
          <svg viewBox="0 0 180 180" className="h-full w-full -rotate-90">
            <circle cx="90" cy="90" r={radius} className="fill-none stroke-slate-800" strokeWidth="14" />
            <motion.circle
              cx="90"
              cy="90"
              r={radius}
              className="fill-none stroke-red-400"
              strokeWidth="14"
              strokeLinecap="round"
              strokeDasharray={circumference}
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset: offset }}
              transition={{ duration: 0.8 }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-4xl font-semibold">{score}</span>
            <span className="text-xs uppercase tracking-wide text-slate-400">{risk?.level || "unknown"}</span>
          </div>
        </div>
        <div className="grid w-full grid-cols-3 gap-2 text-center text-xs">
          {Object.entries(risk?.components || {}).slice(0, 3).map(([key, value]) => (
            <div key={key} className="rounded-lg border border-white/10 bg-white/[0.03] p-3">
              <p className="font-semibold text-slate-200">{value}</p>
              <p className="mt-1 text-slate-500">{key.replaceAll("_", " ")}</p>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}

function TimelineChart({ timeline }) {
  const labels = timeline.map((item) => formatTime(item.timestamp));
  const data = {
    labels,
    datasets: [
      {
        label: "Attack Activity",
        data: timeline.map((item) => item.count),
        borderColor: "#22d3ee",
        backgroundColor: "rgba(34, 211, 238, 0.16)",
        fill: true,
        tension: 0.45,
      },
    ],
  };

  return (
    <Card className="border-white/10 bg-slate-950/70 text-white" title="Attack Timeline">
      <div className="h-72">
        <Line
          data={data}
          options={{
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              x: { grid: { display: false }, ticks: { color: "#94a3b8" } },
              y: { grid: { color: "rgba(148, 163, 184, 0.12)" }, ticks: { color: "#94a3b8" } },
            },
          }}
        />
      </div>
    </Card>
  );
}

function AlertChart({ alerts }) {
  const rows = alerts?.by_severity || [];
  const data = {
    labels: rows.map((row) => row.severity || "unknown"),
    datasets: [
      {
        label: "Alerts",
        data: rows.map((row) => row.count),
        backgroundColor: ["#ef4444", "#f59e0b", "#3b82f6", "#10b981", "#64748b"],
        borderRadius: 6,
      },
    ],
  };

  return (
    <Card className="border-white/10 bg-slate-950/70 text-white" title="Live Alert Distribution">
      <div className="h-72">
        <Bar
          data={data}
          options={{
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
              x: { grid: { display: false }, ticks: { color: "#94a3b8" } },
              y: { grid: { color: "rgba(148, 163, 184, 0.12)" }, ticks: { color: "#94a3b8" } },
            },
          }}
        />
      </div>
    </Card>
  );
}

function ThreatHeatMap({ threatMap }) {
  const cells = threatMap?.indicators || [];
  return (
    <Card className="border-white/10 bg-slate-950/70 text-white" title="Threat Heat Map">
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
        {cells.map((item, index) => (
          <motion.div
            key={`${item.indicator}-${index}`}
            whileHover={{ scale: 1.02 }}
            className={cn("min-h-24 rounded-lg p-3 ring-1", severityClass(item.severity))}
          >
            <p className="truncate text-sm font-semibold">{item.indicator}</p>
            <p className="mt-1 text-xs opacity-75">{item.indicator_type}</p>
            <p className="mt-3 text-lg font-semibold">{item.confidence || 0}%</p>
          </motion.div>
        ))}
      </div>
    </Card>
  );
}

function IncidentTable({ incidents }) {
  const rows = incidents?.recent || [];
  return (
    <Card className="border-white/10 bg-slate-950/70 text-white" title="Incident Table">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[640px] text-left text-sm">
          <thead className="text-xs uppercase text-slate-500">
            <tr>
              <th className="px-3 py-3">ID</th>
              <th className="px-3 py-3">Incident</th>
              <th className="px-3 py-3">Severity</th>
              <th className="px-3 py-3">Status</th>
              <th className="px-3 py-3">Opened</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.incident_key} className="border-t border-white/10">
                <td className="px-3 py-3 font-semibold text-cyan-200">{row.incident_key}</td>
                <td className="px-3 py-3 text-slate-200">{row.title}</td>
                <td className="px-3 py-3">
                  <span className={cn("rounded-full px-2.5 py-1 text-xs font-semibold ring-1", severityClass(row.severity))}>
                    {row.severity}
                  </span>
                </td>
                <td className="px-3 py-3 text-slate-300">{row.status}</td>
                <td className="px-3 py-3 text-slate-400">{formatTime(row.opened_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

function ThreatIntelChat() {
  const [question, setQuestion] = useState("Explain T1078 valid account abuse in this environment.");
  const [messages, setMessages] = useState([
    {
      role: "agent",
      text: "Ask a threat intelligence question. I will call the backend /chat endpoint and return citations when available.",
      citations: [],
    },
  ]);
  const [isSending, setIsSending] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!question.trim()) return;
    const userQuestion = question.trim();
    setMessages((items) => [...items, { role: "user", text: userQuestion }]);
    setQuestion("");
    setIsSending(true);
    try {
      const response = await sendThreatIntelQuestion(userQuestion);
      setMessages((items) => [
        ...items,
        {
          role: "agent",
          text: response.answer,
          citations: response.citations || [],
        },
      ]);
    } catch {
      setMessages((items) => [
        ...items,
        {
          role: "agent",
          text: "Threat intelligence backend is unavailable or requires authentication. The chat panel is wired and ready for /api/v1/chat/.",
          citations: [],
        },
      ]);
    } finally {
      setIsSending(false);
    }
  }

  return (
    <Card className="border-white/10 bg-slate-950/70 text-white" title="Threat Intelligence Chat">
      <div className="flex h-[28rem] flex-col">
        <div className="flex-1 space-y-3 overflow-y-auto pr-1">
          <AnimatePresence initial={false}>
            {messages.map((message, index) => (
              <motion.div
                key={`${message.role}-${index}`}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className={cn("rounded-lg p-3 text-sm", message.role === "user" ? "ml-8 bg-blue-600 text-white" : "mr-8 bg-white/[0.06] text-slate-200")}
              >
                <p>{message.text}</p>
                {message.citations?.length > 0 && (
                  <div className="mt-3 space-y-1">
                    {message.citations.slice(0, 3).map((citation) => (
                      <p key={citation.citation} className="text-xs text-cyan-200">
                        {citation.source} - {citation.title}
                      </p>
                    ))}
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
        <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
          <input
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            className="min-w-0 flex-1 rounded-lg border border-white/10 bg-white/[0.04] px-3 py-2 text-sm outline-none transition placeholder:text-slate-500 focus:border-cyan-400"
            placeholder="Ask about CVEs, MITRE techniques, advisories"
          />
          <button
            type="submit"
            disabled={isSending}
            className="rounded-lg bg-cyan-500 px-3 py-2 text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
            aria-label="Send threat intelligence question"
          >
            {isSending ? <Bot size={18} /> : <Send size={18} />}
          </button>
        </form>
      </div>
    </Card>
  );
}

export default function Dashboard() {
  const [snapshot, setSnapshot] = useState(fallbackDashboard);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [isLive, setIsLive] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);

  async function loadDashboard() {
    setIsRefreshing(true);
    try {
      const data = await fetchDashboardSnapshot();
      setSnapshot(data);
      setIsLive(true);
    } catch {
      setSnapshot((current) => current || fallbackDashboard);
      setIsLive(false);
    } finally {
      setLastUpdated(new Date());
      setIsRefreshing(false);
    }
  }

  useEffect(() => {
    loadDashboard();
    const interval = window.setInterval(loadDashboard, REFRESH_INTERVAL_MS);
    return () => window.clearInterval(interval);
  }, []);

  const overview = snapshot.overview || fallbackDashboard.overview;
  const timeline = snapshot.timeline?.length ? snapshot.timeline : fallbackDashboard.timeline;
  const threatMap = snapshot.threatMap || fallbackDashboard.threatMap;
  const vulnerabilities = snapshot.vulnerabilities?.length ? snapshot.vulnerabilities : fallbackDashboard.vulnerabilities;
  const logs = snapshot.logs?.length ? snapshot.logs : fallbackDashboard.logs;

  const lastLog = logs[0];

  const metrics = useMemo(
    () => [
      {
        icon: ShieldAlert,
        label: "Active Alerts",
        value: overview.active_alerts?.total ?? 0,
        detail: "Open, triaged, investigating",
        tone: "red",
      },
      {
        icon: Radar,
        label: "Risk Score",
        value: overview.risk_score?.score ?? 0,
        detail: `${overview.risk_score?.level || "unknown"} enterprise risk`,
        tone: "amber",
      },
      {
        icon: Server,
        label: "Assets",
        value: overview.assets?.total ?? 0,
        detail: `${overview.assets?.highest_risk?.length || 0} highest-risk surfaced`,
        tone: "blue",
      },
      {
        icon: AlertTriangle,
        label: "Incidents",
        value: overview.incidents?.active ?? 0,
        detail: "Active response cases",
        tone: "emerald",
      },
    ],
    [overview],
  );

  return (
    <div className="min-h-screen space-y-6 rounded-lg bg-slate-950 p-1 text-white">
      <section className="overflow-hidden rounded-lg border border-white/10 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.18),transparent_32%),linear-gradient(135deg,#020617,#0f172a_58%,#111827)] p-5 shadow-2xl shadow-slate-950/40">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <div className="flex items-center gap-2 text-sm font-semibold text-cyan-200">
              <Zap size={16} />
              SOC Command Center
            </div>
            <h1 className="mt-2 text-2xl font-semibold md:text-3xl">SentinelAI Cyber Resilience Dashboard</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
              Live alerts, risk, assets, incidents, vulnerabilities, logs, timeline, and threat intelligence in one operational view.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <span className={cn("rounded-full px-3 py-1 font-semibold ring-1", isLive ? "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30" : "bg-amber-500/15 text-amber-200 ring-amber-400/30")}>
              {isLive ? "Live backend" : "Fallback mode"}
            </span>
            <span className="inline-flex items-center gap-1 rounded-full bg-white/[0.06] px-3 py-1 text-slate-300 ring-1 ring-white/10">
              <Clock3 size={14} />
              Refresh 10s
            </span>
            <span className="rounded-full bg-white/[0.06] px-3 py-1 text-slate-300 ring-1 ring-white/10">
              {isRefreshing ? "Refreshing..." : `Updated ${lastUpdated ? formatTime(lastUpdated) : "pending"}`}
            </span>
          </div>
        </div>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {metrics.map((metric) => (
          <LiveMetricCard key={metric.label} {...metric} />
        ))}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
        <AlertChart alerts={overview.active_alerts} />
        <ConnectedRiskMeter risk={overview.risk_score} />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <TimelineChart timeline={timeline} />
        <ThreatHeatMap threatMap={threatMap} />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.25fr_0.75fr]">
        <IncidentTable incidents={overview.incidents} />
        <Card className="border-white/10 bg-slate-950/70 text-white" title="Top Vulnerabilities">
          <div className="space-y-3">
            {vulnerabilities.slice(0, 5).map((item) => (
              <div key={item.cve_id} className="rounded-lg border border-white/10 bg-white/[0.03] p-3">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-sm font-semibold text-cyan-200">{item.cve_id}</p>
                    <p className="mt-1 text-sm text-slate-300">{item.title}</p>
                  </div>
                  <span className={cn("rounded-full px-2 py-1 text-xs font-semibold ring-1", severityClass(item.severity))}>{item.severity}</span>
                </div>
                <p className="mt-2 text-xs text-slate-500">Priority score {item.priority_score ?? "n/a"}</p>
              </div>
            ))}
          </div>
        </Card>
      </section>

      <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <Card className="border-white/10 bg-slate-950/70 text-white" title="Recent Logs">
          <div className="space-y-3">
            {logs.slice(0, 8).map((log) => (
              <div key={log.event_id} className="rounded-lg border border-white/10 bg-white/[0.03] p-3">
                <div className="flex items-center justify-between gap-3">
                  <p className="truncate text-sm font-semibold text-slate-200">{log.message}</p>
                  <span className={cn("shrink-0 rounded-full px-2 py-1 text-xs font-semibold ring-1", severityClass(log.severity))}>{log.severity}</span>
                </div>
                <div className="mt-2 flex items-center gap-2 text-xs text-slate-500">
                  <Database size={13} />
                  {log.source} / {log.event_type} / {formatTime(log.observed_at)}
                </div>
              </div>
            ))}
          </div>
          {lastLog && <p className="mt-4 text-xs text-slate-500">Newest event: {lastLog.event_id}</p>}
        </Card>
        <ThreatIntelChat />
      </section>
    </div>
  );
}
