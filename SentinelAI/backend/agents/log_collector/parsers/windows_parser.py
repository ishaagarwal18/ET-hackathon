"""Windows event log parser."""

import csv
from io import StringIO

from agents.log_collector.parsers.base import BaseLogParser


class WindowsLogParser(BaseLogParser):
    """Parse exported Windows Event Log CSV content."""

    source_type = "windows"

    def parse(self, content: str):
        records = []
        reader = csv.DictReader(StringIO(content))
        for row in reader:
            records.append(
                self.build_log(
                    event_type=row.get("EventID") or row.get("Event Id") or "windows_event",
                    severity=row.get("Level") or row.get("Keywords"),
                    message=row.get("Message") or row.get("Task Category") or "",
                    observed_at=row.get("TimeCreated") or row.get("Date and Time"),
                    raw=dict(row),
                    hostname=row.get("Computer") or row.get("MachineName"),
                    username=row.get("User") or row.get("Account Name"),
                    process_name=row.get("Process Name"),
                    action=row.get("Task Category"),
                    outcome=row.get("Keywords"),
                )
            )
        return records
