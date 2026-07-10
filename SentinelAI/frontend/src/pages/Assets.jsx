import DataTable from "../components/common/DataTable.jsx";
import StatCard from "../components/common/StatCard.jsx";
import { assetRows } from "../data/mockData.js";

export default function Assets() {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Exposure Inventory</p>
        <h1 className="mt-1 text-2xl font-semibold">Assets</h1>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard label="Total Assets" value="18.6K" change="+4.1%" tone="blue" />
        <StatCard label="Critical Assets" value="942" change="+2.4%" tone="amber" />
        <StatCard label="At Risk" value="119" change="-5.2%" tone="green" />
      </div>
      <DataTable title="Critical Asset Inventory" columns={["ID", "Name", "Type", "Business Criticality", "Status"]} rows={assetRows} />
    </div>
  );
}
