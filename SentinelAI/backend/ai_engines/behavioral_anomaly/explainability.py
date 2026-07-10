"""Explainability helpers for behavioral anomaly results."""

from ai_engines.behavioral_anomaly.constants import FEATURE_NAMES


def build_explanation(features: dict[str, float], model_result: dict) -> list[str]:
    """Generate analyst-readable anomaly explanations."""
    reasons = []

    if features["is_off_hours"]:
        reasons.append("Login occurred outside normal business hours.")
    if features["location_risk"] >= 0.75:
        reasons.append("Location is considered high risk or untrusted.")
    if features["ip_risk"] >= 0.6:
        reasons.append("IP address is external or otherwise elevated risk.")
    if features["failed_login_count"] >= 5:
        reasons.append("Failed login count is significantly elevated.")
    elif features["failed_login_count"] >= 3:
        reasons.append("Failed login count is above normal baseline.")
    if features["usb_activity"]:
        reasons.append("USB activity was observed during the session.")
    if features["download_size_mb"] >= 250:
        reasons.append("Download volume is unusually high.")
    elif features["download_size_mb"] >= 100:
        reasons.append("Download volume is elevated.")
    if features["file_access_count"] >= 150:
        reasons.append("File access count is unusually high.")
    elif features["file_access_count"] >= 80:
        reasons.append("File access count is elevated.")
    if features["process_creation_count"] >= 50:
        reasons.append("Process creation count is unusually high.")
    elif features["process_creation_count"] >= 25:
        reasons.append("Process creation count is elevated.")

    if not reasons and model_result["is_anomaly"]:
        reasons.append("Combined feature pattern deviates from the trained behavioral baseline.")
    if not reasons:
        reasons.append("Activity is consistent with the trained behavioral baseline.")

    return reasons


def calculate_risk_score(features: dict[str, float], anomaly_score: float) -> int:
    """Calculate a 0-100 behavior risk score."""
    weighted_signal = (
        anomaly_score * 42
        + features["is_off_hours"] * 8
        + features["location_risk"] * 10
        + features["ip_risk"] * 10
        + min(features["failed_login_count"] / 8, 1) * 10
        + features["usb_activity"] * 6
        + min(features["download_size_mb"] / 300, 1) * 6
        + min(features["file_access_count"] / 180, 1) * 4
        + min(features["process_creation_count"] / 70, 1) * 4
    )
    return int(max(0, min(100, round(weighted_signal))))


def calculate_confidence_score(features: dict[str, float], anomaly_score: float) -> int:
    """Estimate confidence in the anomaly analysis."""
    populated = sum(1 for name in FEATURE_NAMES if features.get(name) is not None)
    completeness = populated / len(FEATURE_NAMES)
    score_strength = min(abs(anomaly_score - 0.2) * 2.5, 1.0)
    confidence = (0.65 * completeness + 0.35 * score_strength) * 100
    return int(max(1, min(99, round(confidence))))
