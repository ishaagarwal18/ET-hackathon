"""JSON log parser."""

import json

from agents.log_collector.parsers.base import BaseLogParser


class JSONLogParser(BaseLogParser):
    """Parse JSON and JSON Lines logs."""

    source_type = "json"

    def parse(self, content: str):
        records = []
        stripped = content.strip()
        if not stripped:
            return records

        try:
            payload = json.loads(stripped)
            items = payload if isinstance(payload, list) else [payload]
        except json.JSONDecodeError:
            items = [json.loads(line) for line in stripped.splitlines() if line.strip()]

        for item in items:
            records.append(
                self.build_log(
                    event_type=item.get("event_type") or item.get("type") or "json_event",
                    severity=item.get("severity") or item.get("level"),
                    message=item.get("message") or item.get("msg") or "",
                    observed_at=item.get("timestamp") or item.get("time") or item.get("observed_at"),
                    raw=item,
                    hostname=item.get("hostname") or item.get("host"),
                    ip_address=item.get("ip") or item.get("ip_address"),
                    username=item.get("user") or item.get("username"),
                    process_name=item.get("process") or item.get("process_name"),
                    action=item.get("action"),
                    outcome=item.get("outcome"),
                )
            )
        return records
