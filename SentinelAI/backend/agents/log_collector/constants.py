"""Constants for the Log Collector Agent."""

NORMALIZED_LOG_COLLECTION = "logs"

SUPPORTED_LOG_SOURCES = (
    "windows",
    "linux",
    "firewall",
    "json",
    "csv",
    "syslog",
)

SEVERITY_MAP = {
    "0": "critical",
    "1": "critical",
    "2": "high",
    "3": "high",
    "4": "medium",
    "5": "low",
    "6": "informational",
    "7": "informational",
    "critical": "critical",
    "crit": "critical",
    "error": "high",
    "err": "high",
    "warning": "medium",
    "warn": "medium",
    "notice": "low",
    "info": "informational",
    "informational": "informational",
    "debug": "informational",
    "audit success": "informational",
    "audit failure": "high",
}
