"""JSON report exporter."""

import json


class JSONReportExporter:
    """Export incident reports as JSON."""

    extension = "json"
    content_type = "application/json"

    def export(self, *, report: dict, output_path) -> None:
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
