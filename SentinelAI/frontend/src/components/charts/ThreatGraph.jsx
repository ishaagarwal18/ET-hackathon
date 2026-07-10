import Card from "../common/Card.jsx";
import { threatNodes } from "../../data/mockData.js";

const levelClasses = {
  critical: "bg-red-500 shadow-red-500/30",
  high: "bg-amber-500 shadow-amber-500/30",
  medium: "bg-blue-500 shadow-blue-500/30",
  low: "bg-emerald-500 shadow-emerald-500/30",
};

export default function ThreatGraph() {
  return (
    <Card title="Threat Graph" className="h-full">
      <div className="relative h-80 overflow-hidden rounded-lg border border-slate-200 bg-slate-50 dark:border-slate-800 dark:bg-slate-950">
        <svg className="absolute inset-0 h-full w-full" role="presentation">
          <line x1="50%" y1="44%" x2="27%" y2="22%" className="stroke-slate-300 dark:stroke-slate-700" strokeWidth="2" />
          <line x1="50%" y1="44%" x2="72%" y2="27%" className="stroke-slate-300 dark:stroke-slate-700" strokeWidth="2" />
          <line x1="50%" y1="44%" x2="34%" y2="72%" className="stroke-slate-300 dark:stroke-slate-700" strokeWidth="2" />
          <line x1="50%" y1="44%" x2="76%" y2="72%" className="stroke-slate-300 dark:stroke-slate-700" strokeWidth="2" />
        </svg>
        {threatNodes.map((node) => (
          <div
            key={node.id}
            className="absolute -translate-x-1/2 -translate-y-1/2"
            style={{ left: `${node.x}%`, top: `${node.y}%` }}
          >
            <div className={`mx-auto h-4 w-4 rounded-full shadow-lg ${levelClasses[node.level]}`} />
            <p className="mt-2 max-w-28 text-center text-xs font-semibold text-slate-700 dark:text-slate-200">{node.id}</p>
          </div>
        ))}
      </div>
    </Card>
  );
}
