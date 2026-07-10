import { Download, FileBarChart, FileCheck2, FileClock } from "lucide-react";

import Card from "../components/common/Card.jsx";

const reports = [
  { title: "Executive Risk Summary", icon: FileBarChart, cadence: "Weekly", status: "Ready" },
  { title: "Incident Response Review", icon: FileClock, cadence: "Monthly", status: "Draft" },
  { title: "Compliance Evidence Pack", icon: FileCheck2, cadence: "Quarterly", status: "Ready" },
];

export default function Reports() {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Governance Output</p>
        <h1 className="mt-1 text-2xl font-semibold">Reports</h1>
      </div>
      <div className="grid gap-4 lg:grid-cols-3">
        {reports.map((report) => {
          const Icon = report.icon;
          return (
            <Card key={report.title}>
              <Icon className="text-blue-600 dark:text-blue-400" size={28} />
              <h2 className="mt-4 text-base font-semibold text-slate-900 dark:text-white">{report.title}</h2>
              <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">{report.cadence} reporting package</p>
              <div className="mt-5 flex items-center justify-between">
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold dark:bg-slate-800">{report.status}</span>
                <button type="button" aria-label={`Download ${report.title}`} className="rounded-lg border border-slate-200 p-2 text-slate-600 hover:bg-slate-100 dark:border-slate-800 dark:text-slate-300 dark:hover:bg-slate-800">
                  <Download size={17} />
                </button>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
