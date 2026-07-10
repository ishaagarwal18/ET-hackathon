"""Constants for behavioral anomaly detection."""

FEATURE_NAMES = (
    "login_hour",
    "is_off_hours",
    "location_risk",
    "ip_risk",
    "failed_login_count",
    "usb_activity",
    "download_size_mb",
    "file_access_count",
    "process_creation_count",
)

BEHAVIOR_PROFILE_COLLECTION = "behavior_profiles"

DEFAULT_SYNTHETIC_TRAINING_SIZE = 1200
