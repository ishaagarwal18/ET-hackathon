"""Synthetic training data generation for behavioral anomaly detection."""

import random

from ai_engines.behavioral_anomaly.constants import FEATURE_NAMES


def generate_synthetic_user_activity(size: int, seed: int = 42) -> list[list[float]]:
    """Generate realistic baseline activity for Isolation Forest training."""
    random.seed(seed)
    rows = []

    for _ in range(size):
        business_hour = min(23, max(0, int(random.gauss(10.5, 3.0))))
        off_hours = 1.0 if business_hour < 6 or business_hour > 21 else 0.0
        location_risk = max(0.0, min(1.0, random.gauss(0.18, 0.08)))
        ip_risk = max(0.0, min(1.0, random.gauss(0.25, 0.12)))
        failed_logins = max(0, int(random.expovariate(1.6)))
        usb_activity = 1.0 if random.random() < 0.08 else 0.0
        download_size = max(0.0, random.lognormvariate(2.8, 0.65))
        file_access = max(1, int(random.gauss(36, 16)))
        process_creation = max(1, int(random.gauss(12, 6)))

        rows.append(
            [
                float(business_hour),
                off_hours,
                location_risk,
                ip_risk,
                float(failed_logins),
                usb_activity,
                download_size,
                float(file_access),
                float(process_creation),
            ]
        )

    # Add small controlled tails so the model learns operational variance.
    for _ in range(max(20, size // 20)):
        rows.append(
            [
                float(random.choice([5, 22, 23])),
                1.0,
                random.uniform(0.35, 0.75),
                random.uniform(0.45, 0.85),
                float(random.randint(2, 5)),
                1.0 if random.random() < 0.25 else 0.0,
                random.uniform(80, 250),
                float(random.randint(70, 160)),
                float(random.randint(25, 60)),
            ]
        )

    expected_width = len(FEATURE_NAMES)
    return [row for row in rows if len(row) == expected_width]
