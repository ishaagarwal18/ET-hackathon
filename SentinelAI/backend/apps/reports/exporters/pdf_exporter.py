"""PDF report exporter."""

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
except ImportError:
    colors = None
    A4 = None
    getSampleStyleSheet = None
    Paragraph = None
    SimpleDocTemplate = None
    Spacer = None
    Table = None
    TableStyle = None


class PDFReportExporter:
    """Export incident reports as polished PDF documents."""

    extension = "pdf"
    content_type = "application/pdf"

    def export(self, *, report: dict, output_path) -> None:
        if not all((colors, A4, getSampleStyleSheet, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)):
            raise RuntimeError("reportlab is required to generate PDF incident reports.")

        styles = getSampleStyleSheet()
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=42,
            leftMargin=42,
            topMargin=48,
            bottomMargin=42,
            title=f"SentinelAI Incident Report {report['incident']['incident_id']}",
        )
        story = []

        story.append(Paragraph("SentinelAI Incident Report", styles["Title"]))
        story.append(Paragraph(f"Generated: {report['generated_at']}", styles["Normal"]))
        story.append(Spacer(1, 14))

        self._section(story, styles, "Executive Summary", report["executive_summary"])
        self._section(story, styles, "Risk Score", f"{report['risk_score']['score']} - {report['risk_score']['level']}. {report['risk_score'].get('rationale', '')}")

        incident_rows = [
            ["Incident ID", report["incident"]["incident_id"]],
            ["Title", report["incident"]["title"]],
            ["Severity", report["incident"]["severity"]],
            ["Status", report["incident"]["status"]],
            ["Owner", report["incident"]["owner"]],
        ]
        self._table(story, styles, "Incident Details", incident_rows, colors.HexColor("#0f172a"))

        self._table(story, styles, "Timeline", [[item.get("timestamp", ""), item.get("description", "")] for item in report["timeline"]], colors.HexColor("#1d4ed8"))
        self._table(story, styles, "MITRE Mapping", [[item.get("technique_id", ""), item.get("technique_name", ""), item.get("tactic", "")] for item in report["mitre_mapping"]], colors.HexColor("#7c3aed"))
        self._table(story, styles, "Affected Assets", [[item.get("asset_id", ""), item.get("name", ""), item.get("criticality", "")] for item in report["affected_assets"]], colors.HexColor("#b45309"))
        self._table(story, styles, "Response Actions", [[item.get("action", ""), item.get("status", ""), item.get("details", "")] for item in report["response_actions"]], colors.HexColor("#047857"))
        self._table(story, styles, "Recommendations", [[item.get("priority", ""), item.get("description", "")] for item in report["recommendations"]], colors.HexColor("#be123c"))

        doc.build(story)

    def _section(self, story, styles, title: str, body: str) -> None:
        story.append(Paragraph(title, styles["Heading2"]))
        story.append(Paragraph(body or "No details provided.", styles["BodyText"]))
        story.append(Spacer(1, 10))

    def _table(self, story, styles, title: str, rows: list[list], header_color) -> None:
        story.append(Paragraph(title, styles["Heading2"]))
        if not rows:
            story.append(Paragraph("No records provided.", styles["BodyText"]))
            story.append(Spacer(1, 10))
            return

        table = Table(rows, repeatRows=0, hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), header_color),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 12))
