import AttackTimeline from "../components/charts/AttackTimeline.jsx";
import DataTable from "../components/common/DataTable.jsx";
import { incidentRows } from "../data/mockData.js";

export default function Incidents() {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Response Operations</p>
        <h1 className="mt-1 text-2xl font-semibold">Incidents</h1>
      </div>
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <DataTable title="Incident Cases" columns={["ID", "Name", "Priority", "Phase", "Owner"]} rows={incidentRows} />
        <AttackTimeline />
      </div>
    </div>
  );
}
