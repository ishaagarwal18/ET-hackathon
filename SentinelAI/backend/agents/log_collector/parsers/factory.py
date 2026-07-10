"""Parser factory for supported log sources."""

from agents.log_collector.parsers.csv_parser import CSVLogParser
from agents.log_collector.parsers.firewall_parser import FirewallLogParser
from agents.log_collector.parsers.json_parser import JSONLogParser
from agents.log_collector.parsers.linux_parser import LinuxLogParser
from agents.log_collector.parsers.syslog_parser import SyslogParser
from agents.log_collector.parsers.windows_parser import WindowsLogParser


PARSER_REGISTRY = {
    "windows": WindowsLogParser,
    "linux": LinuxLogParser,
    "firewall": FirewallLogParser,
    "json": JSONLogParser,
    "csv": CSVLogParser,
    "syslog": SyslogParser,
}


def get_parser(source_type: str, tenant_id: str, source_name: str | None = None):
    """Return parser instance for a supported source type."""
    parser_class = PARSER_REGISTRY.get(source_type)
    if not parser_class:
        supported = ", ".join(sorted(PARSER_REGISTRY))
        raise ValueError(f"Unsupported log source '{source_type}'. Supported sources: {supported}.")
    return parser_class(tenant_id=tenant_id, source_name=source_name)
