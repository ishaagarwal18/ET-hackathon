"""CSV report exporter."""

import csv


class CSVReportExporter:
    """Export incident report sections as CSV rows."""

    extension = "csv"
    content_type = "text/csv"

    def export(self, *, report: dict, output_path) -> None:
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["section", "key", "value"])
            writer.writerow(["executive_summary", "summary", report["executive_summary"]])
            writer.writerow(["incident", "incident_id", report["incident"]["incident_id"]])
            writer.writerow(["incident", "title", report["incident"]["title"]])
            writer.writerow(["incident", "severity", report["incident"]["severity"]])
            writer.writerow(["incident", "status", report["incident"]["status"]])
            writer.writerow(["risk_score", "score", report["risk_score"]["score"]])
            writer.writerow(["risk_score", "level", report["risk_score"]["level"]])
            writer.writerow(["risk_score", "rationale", report["risk_score"].get("rationale", "")])

            for item in report["timeline"]:
                writer.writerow(["timeline", item.get("timestamp", ""), item.get("description", "")])
            for item in report["mitre_mapping"]:
                writer.writerow(["mitre_mapping", item.get("technique_id", ""), item.get("technique_name", "")])
            for item in report["affected_assets"]:
                writer.writerow(["affected_assets", item.get("asset_id", ""), item.get("name", "")])
            for item in report["response_actions"]:
                writer.writerow(["response_actions", item.get("action", ""), item.get("status", "")])
            for item in report["recommendations"]:
                writer.writerow(["recommendations", item.get("priority", ""), item.get("description", "")])
