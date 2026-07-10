import { Line } from "react-chartjs-2";

import { alertVolume } from "../../data/mockData.js";
import Card from "../common/Card.jsx";

export default function SecurityLineChart() {
  return (
    <Card title="Alert And Threat Volume" className="h-full">
      <div className="h-72">
        <Line
          data={alertVolume}
          options={{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: "bottom",
                labels: { boxWidth: 10, usePointStyle: true },
              },
            },
            scales: {
              x: { grid: { display: false } },
              y: { grid: { color: "rgba(148, 163, 184, 0.16)" } },
            },
          }}
        />
      </div>
    </Card>
  );
}
