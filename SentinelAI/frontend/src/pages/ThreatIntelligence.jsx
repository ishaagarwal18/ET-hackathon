import RiskMeter from "../components/charts/RiskMeter.jsx";
import ThreatGraph from "../components/charts/ThreatGraph.jsx";
import Card from "../components/common/Card.jsx";

const indicators = ["APT credential harvesting", "Cloud token replay", "Phishing infrastructure", "Data staging host"];

export default function ThreatIntelligence() {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Intel Fusion</p>
        <h1 className="mt-1 text-2xl font-semibold">Threat Intelligence</h1>
      </div>
      <div className="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
        <ThreatGraph />
        <RiskMeter score={81} />
      </div>
      <Card title="Priority Indicators">
        <div className="grid gap-3 md:grid-cols-2">
          {indicators.map((indicator) => (
            <div key={indicator} className="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
              <p className="font-semibold text-slate-900 dark:text-white">{indicator}</p>
              <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Correlated across telemetry, asset exposure, and incident context.</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
