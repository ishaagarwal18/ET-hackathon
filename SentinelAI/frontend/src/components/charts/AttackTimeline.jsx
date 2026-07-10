import { attackEvents } from "../../data/mockData.js";
import Card from "../common/Card.jsx";

const severityClasses = {
  Critical: "bg-red-100 text-red-700 dark:bg-red-950/60 dark:text-red-300",
  High: "bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300",
  Medium: "bg-blue-100 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300",
};

export default function AttackTimeline() {
  return (
    <Card title="Attack Timeline">
      <div className="space-y-4">
        {attackEvents.map((event, index) => (
          <div key={event.time} className="relative flex gap-4">
            <div className="flex w-14 shrink-0 justify-end text-xs font-semibold text-slate-500 dark:text-slate-400">
              {event.time}
            </div>
            <div className="relative">
              <span className="absolute left-1.5 top-5 h-full w-px bg-slate-200 dark:bg-slate-800" />
              <span className="relative z-10 block h-3.5 w-3.5 rounded-full bg-blue-600 ring-4 ring-blue-100 dark:ring-blue-950" />
            </div>
            <div className={index === attackEvents.length - 1 ? "" : "pb-4"}>
              <div className="flex flex-wrap items-center gap-2">
                <p className="text-sm font-semibold text-slate-900 dark:text-white">{event.title}</p>
                <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${severityClasses[event.severity]}`}>
                  {event.severity}
                </span>
              </div>
              <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{event.source}</p>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}
