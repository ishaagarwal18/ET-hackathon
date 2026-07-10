import { Doughnut } from "react-chartjs-2";

import { riskBreakdown } from "../../data/mockData.js";
import Card from "../common/Card.jsx";

export default function RiskMeter({ score = 72 }) {
  return (
    <Card title="Risk Meter" className="h-full">
      <div className="relative mx-auto h-56 max-w-72">
        <Doughnut
          data={riskBreakdown}
          options={{
            cutout: "72%",
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: { enabled: true },
            },
          }}
        />
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-semibold text-slate-950 dark:text-white">{score}</span>
          <span className="text-xs font-medium uppercase text-slate-500 dark:text-slate-400">Elevated</span>
        </div>
      </div>
      <div className="mt-5 grid grid-cols-2 gap-2 text-xs text-slate-500 dark:text-slate-400">
        {riskBreakdown.labels.map((label, index) => (
          <div key={label} className="flex items-center gap-2">
            <span
              className="h-2.5 w-2.5 rounded-full"
              style={{ backgroundColor: riskBreakdown.datasets[0].backgroundColor[index] }}
            />
            {label}
          </div>
        ))}
      </div>
    </Card>
  );
}
