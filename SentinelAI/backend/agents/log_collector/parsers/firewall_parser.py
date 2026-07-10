"""Firewall log parser."""

import csv
from io import StringIO

from agents.log_collector.parsers.base import BaseLogParser


class FirewallLogParser(BaseLogParser):
    """Parse common firewall CSV exports."""

    source_type = "firewall"

    def parse(self, content: str):
        records = []
        reader = csv.DictReader(StringIO(content))
        for row in reader:
            action = row.get("action") or row.get("Action")
            severity = "high" if str(action).lower() in ("deny", "blocked", "drop") else "low"
            records.append(
                self.build_log(
                    event_type=row.get("event_type") or "firewall_traffic",
                    severity=row.get("severity") or severity,
                    message=row.get("message") or f"{action} traffic from {row.get('src_ip')} to {row.get('dst_ip')}",
                    observed_at=row.get("timestamp") or row.get("time"),
                    raw=dict(row),
                    hostname=row.get("device") or row.get("hostname"),
                    ip_address=row.get("src_ip"),
                    action=action,
                    outcome="blocked" if severity == "high" else "allowed",
                    normalized={
                        "src_ip": row.get("src_ip"),
                        "dst_ip": row.get("dst_ip"),
                        "src_port": row.get("src_port"),
                        "dst_port": row.get("dst_port"),
                        "protocol": row.get("protocol"),
                    },
                )
            )
        return records
