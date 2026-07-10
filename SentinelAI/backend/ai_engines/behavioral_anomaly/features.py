"""Feature engineering for user behavioral anomaly detection."""

from datetime import UTC, datetime
from ipaddress import ip_address
from typing import Any

from ai_engines.behavioral_anomaly.constants import FEATURE_NAMES


def parse_login_time(value: str | datetime) -> datetime:
    """Parse login time into a timezone-aware datetime."""
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)

    text = str(value).strip()
    for suffix in ("Z", "+00:00"):
        if text.endswith(suffix):
            text = text.removesuffix(suffix)
            break

    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        parsed = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def score_location(location: str) -> float:
    """Assign a conservative risk score for location strings."""
    normalized = location.strip().lower()
    if not normalized:
        return 0.8
    elevated_terms = ("unknown", "tor", "vpn", "proxy", "foreign", "untrusted")
    if any(term in normalized for term in elevated_terms):
        return 1.0
    return 0.15


def score_ip(value: str) -> float:
    """Score IP address risk using local/private/reserved hints."""
    try:
        parsed = ip_address(value)
    except ValueError:
        return 1.0
    if parsed.is_private:
        return 0.1
    if parsed.is_loopback or parsed.is_reserved or parsed.is_multicast:
        return 0.4
    return 0.65


def extract_features(payload: dict[str, Any]) -> dict[str, float]:
    """Convert behavior payload into numeric model features."""
    login_time = parse_login_time(payload["login_time"])
    login_hour = float(login_time.hour)

    features = {
        "login_hour": login_hour,
        "is_off_hours": 1.0 if login_time.hour < 6 or login_time.hour > 21 else 0.0,
        "location_risk": score_location(payload.get("location", "")),
        "ip_risk": score_ip(payload.get("ip", "")),
        "failed_login_count": float(payload.get("failed_login_count", 0)),
        "usb_activity": 1.0 if payload.get("usb_activity", False) else 0.0,
        "download_size_mb": float(payload.get("download_size", 0)),
        "file_access_count": float(payload.get("file_access", 0)),
        "process_creation_count": float(payload.get("process_creation", 0)),
    }
    return {name: features[name] for name in FEATURE_NAMES}


def feature_vector(features: dict[str, float]) -> list[float]:
    """Return feature vector in the engine's canonical order."""
    return [features[name] for name in FEATURE_NAMES]
