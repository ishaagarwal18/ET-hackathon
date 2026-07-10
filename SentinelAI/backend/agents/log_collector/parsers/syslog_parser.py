"""Syslog parser."""

import re

from agents.log_collector.parsers.base import BaseLogParser


SYSLOG_PATTERN = re.compile(
    r"^(?:<(?P<priority>\d+)>)?(?P<timestamp>[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<host>\S+)\s+(?P<process>[\w.\-/]+)(?:\[(?P<pid>\d+)\])?:\s*(?P<message>.*)$"
)


class SyslogParser(BaseLogParser):
    """Parse RFC3164-style syslog lines."""

    source_type = "syslog"

    def parse(self, content: str):
        records = []
        for line in content.splitlines():
            if not line.strip():
                continue
            match = SYSLOG_PATTERN.match(line.strip())
            raw = {"line": line}
            if not match:
                records.append(self.build_log(event_type="syslog_event", severity=None, message=line, raw=raw))
                continue

            data = match.groupdict()
            raw.update(data)
            severity = int(data["priority"]) % 8 if data.get("priority") else None
            records.append(
                self.build_log(
                    event_type="syslog_event",
                    severity=severity,
                    message=data["message"],
                    observed_at=data["timestamp"],
                    raw=raw,
                    hostname=data["host"],
                    process_name=data["process"],
                    metadata={"pid": data.get("pid")},
                )
            )
        return records
