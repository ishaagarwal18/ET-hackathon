import { useCallback, useMemo, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  Handle,
  MarkerType,
  MiniMap,
  Position,
  addEdge,
  useEdgesState,
  useNodesState,
} from "reactflow";
import "reactflow/dist/style.css";
import { motion } from "framer-motion";
import {
  Activity,
  AlertTriangle,
  Flame,
  Network,
  Play,
  RotateCcw,
  Server,
  Shield,
  SquareUser,
  SwitchCamera,
} from "lucide-react";

import Card from "../components/common/Card.jsx";
import { cn } from "../utils/cn.js";

const nodeIcon = {
  server: Server,
  firewall: Shield,
  switch: SwitchCamera,
  user: SquareUser,
};

const nodeStyles = {
  server: "border-blue-400/30 bg-blue-500/10 text-blue-100",
  firewall: "border-emerald-400/30 bg-emerald-500/10 text-emerald-100",
  switch: "border-cyan-400/30 bg-cyan-500/10 text-cyan-100",
  user: "border-amber-400/30 bg-amber-500/10 text-amber-100",
};

function TwinNode({ data }) {
  const Icon = nodeIcon[data.type] || Server;

  return (
    <div
      className={cn(
        "min-w-44 rounded-lg border p-3 shadow-2xl shadow-slate-950/30 backdrop-blur",
        nodeStyles[data.type],
        data.compromised && "ring-2 ring-red-400",
        data.active && "animate-pulse",
      )}
    >
      <Handle type="target" position={Position.Left} className="!border-slate-950 !bg-cyan-300" />
      <div className="flex items-center gap-3">
        <div className="rounded-lg bg-slate-950/70 p-2">
          <Icon size={18} />
        </div>
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold">{data.label}</p>
          <p className="text-xs text-slate-400">{data.meta}</p>
        </div>
      </div>
      <div className="mt-3 flex items-center justify-between text-xs">
        <span className="text-slate-400">{data.zone}</span>
        <span
          className={cn(
            "rounded-full px-2 py-0.5 font-semibold",
            data.compromised ? "bg-red-500/20 text-red-200" : "bg-emerald-500/15 text-emerald-200",
          )}
        >
          {data.compromised ? "Compromised" : "Healthy"}
        </span>
      </div>
      <Handle type="source" position={Position.Right} className="!border-slate-950 !bg-cyan-300" />
    </div>
  );
}

const nodeTypes = { twinNode: TwinNode };

const baseNodes = [
  { id: "user-admin", type: "twinNode", position: { x: 20, y: 120 }, data: { type: "user", label: "Admin User", meta: "Privileged identity", zone: "Identity" } },
  { id: "user-analyst", type: "twinNode", position: { x: 20, y: 330 }, data: { type: "user", label: "SOC Analyst", meta: "Read/write console", zone: "Identity" } },
  { id: "fw-edge", type: "twinNode", position: { x: 320, y: 80 }, data: { type: "firewall", label: "Edge Firewall", meta: "Ingress filtering", zone: "Perimeter" } },
  { id: "sw-core", type: "twinNode", position: { x: 610, y: 210 }, data: { type: "switch", label: "Core Switch", meta: "East-west routing", zone: "Network" } },
  { id: "srv-auth", type: "twinNode", position: { x: 900, y: 50 }, data: { type: "server", label: "Auth Server", meta: "SSO and IAM", zone: "Production" } },
  { id: "srv-app", type: "twinNode", position: { x: 900, y: 230 }, data: { type: "server", label: "App Server", meta: "Customer portal", zone: "Production" } },
  { id: "srv-db", type: "twinNode", position: { x: 900, y: 420 }, data: { type: "server", label: "Data Vault", meta: "Sensitive records", zone: "Restricted" } },
];

const baseEdges = [
  { id: "e1", source: "user-admin", target: "fw-edge", label: "VPN", type: "smoothstep" },
  { id: "e2", source: "user-analyst", target: "fw-edge", label: "SOC access", type: "smoothstep" },
  { id: "e3", source: "fw-edge", target: "sw-core", label: "filtered", type: "smoothstep" },
  { id: "e4", source: "sw-core", target: "srv-auth", label: "auth", type: "smoothstep" },
  { id: "e5", source: "sw-core", target: "srv-app", label: "app", type: "smoothstep" },
  { id: "e6", source: "sw-core", target: "srv-db", label: "data", type: "smoothstep" },
  { id: "e7", source: "srv-app", target: "srv-db", label: "query", type: "smoothstep" },
].map((edge) => ({
  ...edge,
  style: { stroke: "#475569", strokeWidth: 2 },
  labelStyle: { fill: "#94a3b8", fontSize: 12 },
}));

const scenarios = {
  credential_compromise: {
    name: "Credential Compromise",
    risk: "Critical",
    path: ["user-admin", "fw-edge", "sw-core", "srv-auth", "srv-db"],
    events: [
      "Valid account used from untrusted location",
      "VPN session established through edge firewall",
      "Identity server queried for privileged groups",
      "Sensitive data vault access attempted",
    ],
  },
  malware_lateral_movement: {
    name: "Malware Lateral Movement",
    risk: "High",
    path: ["user-analyst", "fw-edge", "sw-core", "srv-app", "srv-db"],
    events: [
      "Analyst workstation executes suspicious payload",
      "Connection traverses perimeter controls",
      "Application server receives abnormal process activity",
      "Database query volume spikes",
    ],
  },
  perimeter_probe: {
    name: "Perimeter Probe",
    risk: "Medium",
    path: ["fw-edge", "sw-core", "srv-app"],
    events: [
      "External scan touches firewall rule boundary",
      "Core switch observes unusual traffic pattern",
      "Application server receives malformed requests",
    ],
  },
};

function applyScenario(nodes, edges, scenario) {
  const activePairs = new Set();
  for (let index = 0; index < scenario.path.length - 1; index += 1) {
    activePairs.add(`${scenario.path[index]}:${scenario.path[index + 1]}`);
  }
  const activeNodes = new Set(scenario.path);

  return {
    nodes: nodes.map((node) => ({
      ...node,
      data: {
        ...node.data,
        active: activeNodes.has(node.id),
        compromised: activeNodes.has(node.id) && !node.id.startsWith("fw"),
      },
    })),
    edges: edges.map((edge) => {
      const active = activePairs.has(`${edge.source}:${edge.target}`);
      return {
        ...edge,
        animated: active,
        markerEnd: active ? { type: MarkerType.ArrowClosed, color: "#ef4444" } : undefined,
        style: {
          stroke: active ? "#ef4444" : "#475569",
          strokeWidth: active ? 4 : 2,
          filter: active ? "drop-shadow(0 0 8px rgba(239,68,68,0.8))" : "none",
        },
      };
    }),
  };
}

export default function CyberDigitalTwin() {
  const [nodes, setNodes, onNodesChange] = useNodesState(baseNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(baseEdges);
  const [selectedScenario, setSelectedScenario] = useState("credential_compromise");
  const [activeScenario, setActiveScenario] = useState(null);
  const [logs, setLogs] = useState(["Digital twin loaded in simulation mode. No real infrastructure is connected."]);

  const scenario = scenarios[selectedScenario];

  const onConnect = useCallback((params) => setEdges((items) => addEdge({ ...params, type: "smoothstep" }, items)), [setEdges]);

  const stats = useMemo(() => {
    const compromised = nodes.filter((node) => node.data.compromised).length;
    return {
      total: nodes.length,
      compromised,
      connections: edges.length,
      risk: activeScenario?.risk || "None",
    };
  }, [nodes, edges, activeScenario]);

  function runSimulation() {
    const result = applyScenario(baseNodes, baseEdges, scenario);
    setNodes(result.nodes);
    setEdges(result.edges);
    setActiveScenario(scenario);
    setLogs([
      `Simulation started: ${scenario.name}`,
      ...scenario.events.map((event, index) => `Step ${index + 1}: ${event}`),
      "Simulation complete. No real users, devices, servers, or controls were changed.",
    ]);
  }

  function resetSimulation() {
    setNodes(baseNodes);
    setEdges(baseEdges);
    setActiveScenario(null);
    setLogs(["Digital twin reset. Environment returned to healthy simulation baseline."]);
  }

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-800 bg-slate-950 p-5 text-white shadow-2xl shadow-slate-950/30">
        <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
          <div>
            <div className="flex items-center gap-2 text-sm font-semibold text-cyan-300">
              <Network size={17} />
              Cyber Digital Twin
            </div>
            <h1 className="mt-2 text-2xl font-semibold md:text-3xl">Simulated Infrastructure Attack Movement</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
              Visualize servers, firewalls, switches, users, and connections. Run simulated attacks with animated paths without touching real infrastructure.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <select
              value={selectedScenario}
              onChange={(event) => setSelectedScenario(event.target.value)}
              className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 outline-none"
            >
              {Object.entries(scenarios).map(([key, item]) => (
                <option key={key} value={key}>
                  {item.name}
                </option>
              ))}
            </select>
            <button
              type="button"
              onClick={runSimulation}
              className="inline-flex items-center gap-2 rounded-lg bg-red-500 px-3 py-2 text-sm font-semibold text-white transition hover:bg-red-400"
            >
              <Play size={16} />
              Simulate Attack
            </button>
            <button
              type="button"
              onClick={resetSimulation}
              className="inline-flex items-center gap-2 rounded-lg border border-slate-700 px-3 py-2 text-sm font-semibold text-slate-200 transition hover:bg-slate-900"
            >
              <RotateCcw size={16} />
              Reset
            </button>
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-4">
        {[
          ["Nodes", stats.total, Server],
          ["Connections", stats.connections, Network],
          ["Compromised", stats.compromised, Flame],
          ["Scenario Risk", stats.risk, AlertTriangle],
        ].map(([label, value, Icon]) => (
          <motion.div
            key={label}
            whileHover={{ y: -2 }}
            className="rounded-lg border border-slate-800 bg-slate-950 p-4 text-white shadow-lg"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold uppercase text-slate-500">{label}</p>
                <p className="mt-2 text-2xl font-semibold">{value}</p>
              </div>
              <Icon className="text-cyan-300" size={22} />
            </div>
          </motion.div>
        ))}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.5fr_0.5fr]">
        <div className="h-[620px] overflow-hidden rounded-lg border border-slate-800 bg-slate-950">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            fitView
            fitViewOptions={{ padding: 0.18 }}
            className="digital-twin-flow"
          >
            <Background color="#334155" gap={22} />
            <Controls className="!border-slate-800 !bg-slate-900 !text-white" />
            <MiniMap
              nodeColor={(node) => (node.data?.compromised ? "#ef4444" : "#06b6d4")}
              maskColor="rgba(2, 6, 23, 0.72)"
              className="!border !border-slate-800 !bg-slate-900"
            />
          </ReactFlow>
        </div>

        <Card className="border-slate-800 bg-slate-950 text-white" title="Simulation Logs">
          <div className="space-y-3">
            {logs.map((log, index) => (
              <motion.div
                key={`${log}-${index}`}
                initial={{ opacity: 0, x: 12 }}
                animate={{ opacity: 1, x: 0 }}
                className="rounded-lg border border-slate-800 bg-slate-900/70 p-3"
              >
                <div className="flex gap-2">
                  <Activity className="mt-0.5 shrink-0 text-cyan-300" size={15} />
                  <p className="text-sm leading-6 text-slate-300">{log}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </Card>
      </section>
    </div>
  );
}
