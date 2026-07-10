"""Incident report generation service."""

from pathlib import Path

from django.conf import settings

from apps.reports.builders.incident_report_builder import IncidentReportBuilder
from apps.reports.exporters.csv_exporter import CSVReportExporter
from apps.reports.exporters.json_exporter import JSONReportExporter
from apps.reports.exporters.pdf_exporter import PDFReportExporter


class IncidentReportService:
    """Generate downloadable incident reports."""

    exporters = {
        "pdf": PDFReportExporter,
        "csv": CSVReportExporter,
        "json": JSONReportExporter,
    }

    def __init__(self, output_dir: Path | None = None):
        self.output_dir = output_dir or settings.BASE_DIR / "generated_reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.builder = IncidentReportBuilder()

    def generate(self, *, tenant_id: str, requested_by: str, payload: dict, formats: list[str]) -> dict:
        """Generate requested report formats and return download metadata."""
        report = self.builder.build(tenant_id=tenant_id, requested_by=requested_by, payload=payload)
        files = []

        for export_format in formats:
            exporter = self.exporters[export_format]()
            filename = f"incident-report-{report['incident']['incident_id']}-{report['report_id']}.{exporter.extension}"
            output_path = self.output_dir / filename
            exporter.export(report=report, output_path=output_path)
            files.append(
                {
                    "format": export_format,
                    "filename": filename,
                    "content_type": exporter.content_type,
                    "download_url": f"/api/v1/reports/download/{filename}/",
                }
            )

        return {
            "report_id": report["report_id"],
            "incident_id": report["incident"]["incident_id"],
            "generated_at": report["generated_at"],
            "files": files,
            "report": report,
        }

    def resolve_download(self, filename: str) -> tuple[Path, str]:
        """Resolve a generated report path safely."""
        safe_name = Path(filename).name
        path = (self.output_dir / safe_name).resolve()
        output_root = self.output_dir.resolve()
        if output_root not in path.parents and path != output_root:
            raise ValueError("Invalid report path.")
        if not path.exists() or not path.is_file():
            raise FileNotFoundError("Report file not found.")
        return path, self._content_type(path.suffix.lower())

    def _content_type(self, suffix: str) -> str:
        return {
            ".pdf": "application/pdf",
            ".csv": "text/csv",
            ".json": "application/json",
        }.get(suffix, "application/octet-stream")
