"""CSV log parser."""

import csv
from io import StringIO

from agents.log_collector.parsers.base import BaseLogParser


class CSVLogParser(BaseLogParser):
    """Parse CSV logs with common security-event columns."""

    source_type = "csv"

    def parse(self, content: str):
        records = []
        reader = csv.DictReader(StringIO(content))
        for row in reader:
            records.append(
                self.build_log(
                    event_type=row.get("event_type") or row.get("type") or row.get("category") or "csv_event",
                    severity=row.get("severity") or row.get("level"),
                    message=row.get("message") or row.get("description") or "",
                    observed_at=row.get("timestamp") or row.get("time") or row.get("observed_at"),
                    raw=dict(row),
                    hostname=row.get("hostname") or row.get("host"),
                    ip_address=row.get("ip") or row.get("ip_address") or row.get("src_ip"),
                    username=row.get("user") or row.get("username"),
                    process_name=row.get("process") or row.get("process_name"),
                    action=row.get("action"),
                    outcome=row.get("outcome"),
                )
            )
        return records
