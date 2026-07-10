import { ArrowDownRight, ArrowUpRight } from "lucide-react";

import Card from "./Card.jsx";

const toneClasses = {
  red: "bg-red-50 text-red-700 dark:bg-red-950/50 dark:text-red-300",
  amber: "bg-amber-50 text-amber-700 dark:bg-amber-950/50 dark:text-amber-300",
  green: "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300",
  blue: "bg-blue-50 text-blue-700 dark:bg-blue-950/50 dark:text-blue-300",
};

export default function StatCard({ label, value, change, tone }) {
  const isNegative = change.startsWith("-");

  return (
    <Card className="min-h-32">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{label}</p>
          <p className="mt-3 text-3xl font-semibold text-slate-950 dark:text-white">{value}</p>
        </div>
        <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold ${toneClasses[tone]}`}>
          {isNegative ? <ArrowDownRight size={14} /> : <ArrowUpRight size={14} />}
          {change}
        </span>
      </div>
    </Card>
  );
}
