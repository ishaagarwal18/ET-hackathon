import DataTable from "../components/common/DataTable.jsx";
import StatCard from "../components/common/StatCard.jsx";
import { alertRows } from "../data/mockData.js";

export default function Alerts() {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Detection Queue</p>
        <h1 className="mt-1 text-2xl font-semibold">Alerts</h1>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard label="Critical" value="86" change="+9.1%" tone="red" />
        <StatCard label="Triaged" value="412" change="+3.7%" tone="blue" />
        <StatCard label="False Positive Rate" value="7.4%" change="-1.8%" tone="green" />
      </div>
      <DataTable title="Alert Work Queue" columns={["ID", "Title", "Severity", "Source", "Status"]} rows={alertRows} />
    </div>
  );
}
