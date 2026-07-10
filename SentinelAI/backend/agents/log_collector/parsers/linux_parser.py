"""Linux log parser."""

import re

from agents.log_collector.parsers.base import BaseLogParser


LINUX_PATTERN = re.compile(
    r"^(?P<timestamp>[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<host>\S+)\s+(?P<process>[\w.\-/]+)(?:\[(?P<pid>\d+)\])?:\s*(?P<message>.*)$"
)


class LinuxLogParser(BaseLogParser):
    """Parse common Linux auth/syslog lines."""

    source_type = "linux"

    def parse(self, content: str):
        records = []
        for line in content.splitlines():
            if not line.strip():
                continue
            match = LINUX_PATTERN.match(line.strip())
            raw = {"line": line}
            if not match:
                records.append(self.build_log(event_type="linux_event", severity=None, message=line, raw=raw))
                continue

            data = match.groupdict()
            message = data["message"]
            lowered = message.lower()
            severity = "high" if "failed" in lowered or "invalid" in lowered else "informational"
            records.append(
                self.build_log(
                    event_type="linux_auth" if "ssh" in data["process"].lower() else "linux_event",
                    severity=severity,
                    message=message,
                    observed_at=data["timestamp"],
                    raw={**raw, **data},
                    hostname=data["host"],
                    process_name=data["process"],
                    outcome="failure" if severity == "high" else "success",
                    metadata={"pid": data.get("pid")},
                )
            )
        return records
