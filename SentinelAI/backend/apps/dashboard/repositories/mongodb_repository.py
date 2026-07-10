"""MongoDB aggregation repository for dashboard APIs."""

from datetime import UTC, datetime, timedelta
from typing import Any

from database.mongodb.collections import COLLECTIONS


class DashboardMongoRepository:
    """Read-optimized dashboard aggregation repository."""

    def __init__(self):
        from core.mongodb import get_mongo_database

        self.database = get_mongo_database()

    def active_alerts(self, *, tenant_id: str) -> dict[str, Any]:
        """Aggregate active alert cards by severity and status."""
        pipeline = [
            {
                "$match": {
                    "tenant_id": tenant_id,
                    "deleted_at": None,
                    "status": {"$in": ["new", "triaged", "investigating"]},
                }
            },
            {
                "$group": {
                    "_id": {"severity": "$severity", "status": "$status"},
                    "count": {"$sum": 1},
                }
            },
            {
                "$group": {
                    "_id": "$_id.severity",
                    "count": {"$sum": "$count"},
                    "statuses": {
                        "$push": {
                            "status": "$_id.status",
                            "count": "$count",
                        }
                    },
                }
            },
            {"$project": {"_id": 0, "severity": "$_id", "count": 1, "statuses": 1}},
        ]
        rows = list(self.database[COLLECTIONS["alerts"]].aggregate(pipeline, allowDiskUse=False))
        total = sum(row["count"] for row in rows)
        return {"total": total, "by_severity": rows}

    def risk_score(self, *, tenant_id: str) -> dict[str, Any]:
        """Aggregate risk score from assets, alerts, incidents, and behavior profiles."""
        asset_pipeline = [
            {"$match": {"tenant_id": tenant_id, "deleted_at": None}},
            {
                "$group": {
                    "_id": None,
                    "average_asset_risk": {"$avg": "$risk_score"},
                    "critical_assets": {
                        "$sum": {"$cond": [{"$eq": ["$criticality", "critical"]}, 1, 0]}
                    },
                }
            },
        ]
        alert_pipeline = [
            {
                "$match": {
                    "tenant_id": tenant_id,
                    "deleted_at": None,
                    "status": {"$in": ["new", "triaged", "investigating"]},
                }
            },
            {
                "$group": {
                    "_id": "$severity",
                    "count": {"$sum": 1},
                }
            },
        ]
        behavior_pipeline = [
            {"$match": {"tenant_id": tenant_id, "deleted_at": None, "status": {"$in": ["active", "learning"]}}},
            {"$group": {"_id": None, "average_behavior_risk": {"$avg": "$risk_score"}}},
        ]

        asset_row = next(iter(self.database[COLLECTIONS["assets"]].aggregate(asset_pipeline)), {})
        alert_rows = list(self.database[COLLECTIONS["alerts"]].aggregate(alert_pipeline))
        behavior_row = next(iter(self.database[COLLECTIONS["behavior_profiles"]].aggregate(behavior_pipeline)), {})

        severity_weights = {"critical": 9, "high": 6, "medium": 3, "low": 1, "informational": 0.5}
        alert_pressure = min(
            sum(severity_weights.get(row["_id"], 1) * row["count"] for row in alert_rows),
            100,
        )
        asset_risk = float(asset_row.get("average_asset_risk") or 0)
        behavior_risk = float(behavior_row.get("average_behavior_risk") or 0)
        score = round(min((asset_risk * 0.35) + (alert_pressure * 0.4) + (behavior_risk * 0.25), 100), 2)

        return {
            "score": score,
            "level": self._risk_level(score),
            "components": {
                "asset_risk": round(asset_risk, 2),
                "alert_pressure": round(alert_pressure, 2),
                "behavior_risk": round(behavior_risk, 2),
                "critical_assets": int(asset_row.get("critical_assets") or 0),
            },
        }

    def assets(self, *, tenant_id: str) -> dict[str, Any]:
        """Aggregate assets by type, status, and criticality."""
        pipeline = [
            {"$match": {"tenant_id": tenant_id, "deleted_at": None}},
            {
                "$facet": {
                    "total": [{"$count": "count"}],
                    "by_type": [{"$group": {"_id": "$asset_type", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}],
                    "by_status": [{"$group": {"_id": "$status", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}],
                    "by_criticality": [{"$group": {"_id": "$criticality", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}],
                    "highest_risk": [
                        {"$sort": {"risk_score": -1, "updated_at": -1}},
                        {"$limit": 5},
                        {"$project": {"_id": 0, "asset_key": 1, "name": 1, "asset_type": 1, "risk_score": 1, "criticality": 1}},
                    ],
                }
            },
        ]
        row = next(iter(self.database[COLLECTIONS["assets"]].aggregate(pipeline)), {})
        return {
            "total": self._facet_count(row, "total"),
            "by_type": self._group_rows(row.get("by_type", [])),
            "by_status": self._group_rows(row.get("by_status", [])),
            "by_criticality": self._group_rows(row.get("by_criticality", [])),
            "highest_risk": row.get("highest_risk", []),
        }

    def incidents(self, *, tenant_id: str) -> dict[str, Any]:
        """Aggregate incidents by status, severity, and priority."""
        pipeline = [
            {"$match": {"tenant_id": tenant_id, "deleted_at": None}},
            {
                "$facet": {
                    "active": [{"$match": {"status": {"$ne": "closed"}}}, {"$count": "count"}],
                    "by_status": [{"$group": {"_id": "$status", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}],
                    "by_severity": [{"$group": {"_id": "$severity", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}],
                    "recent": [
                        {"$sort": {"opened_at": -1, "updated_at": -1}},
                        {"$limit": 5},
                        {"$project": {"_id": 0, "incident_key": 1, "title": 1, "severity": 1, "status": 1, "priority": 1, "opened_at": 1}},
                    ],
                }
            },
        ]
        row = next(iter(self.database[COLLECTIONS["incidents"]].aggregate(pipeline)), {})
        return {
            "active": self._facet_count(row, "active"),
            "by_status": self._group_rows(row.get("by_status", [])),
            "by_severity": self._group_rows(row.get("by_severity", [])),
            "recent": [self._serialize_dates(item) for item in row.get("recent", [])],
        }

    def top_vulnerabilities(self, *, tenant_id: str, limit: int = 10) -> list[dict[str, Any]]:
        """Return top CVEs by exploitation and severity signals."""
        pipeline = [
            {"$match": {"tenant_id": tenant_id, "deleted_at": None, "status": {"$ne": "archived"}}},
            {
                "$addFields": {
                    "priority_score": {
                        "$add": [
                            {"$ifNull": ["$cvss.score", 0]},
                            {"$multiply": [{"$ifNull": ["$exploitation.epss_score", 0]}, 10]},
                            {"$cond": [{"$eq": ["$exploitation.known_exploited", True]}, 5, 0]},
                        ]
                    }
                }
            },
            {"$sort": {"priority_score": -1, "published_at": -1}},
            {"$limit": limit},
            {
                "$project": {
                    "_id": 0,
                    "cve_id": 1,
                    "title": 1,
                    "severity": 1,
                    "status": 1,
                    "cvss": 1,
                    "exploitation": 1,
                    "priority_score": {"$round": ["$priority_score", 2]},
                    "published_at": 1,
                }
            },
        ]
        return [self._serialize_dates(row) for row in self.database[COLLECTIONS["cve"]].aggregate(pipeline)]

    def recent_logs(self, *, tenant_id: str, limit: int = 20) -> list[dict[str, Any]]:
        """Return recent normalized logs."""
        pipeline = [
            {"$match": {"tenant_id": tenant_id, "deleted_at": None}},
            {"$sort": {"observed_at": -1, "created_at": -1}},
            {"$limit": limit},
            {
                "$project": {
                    "_id": 0,
                    "event_id": 1,
                    "source": {"$ifNull": ["$source", "$source_type"]},
                    "event_type": 1,
                    "severity": 1,
                    "message": 1,
                    "status": 1,
                    "observed_at": 1,
                    "asset": 1,
                    "user": 1,
                }
            },
        ]
        return [self._serialize_dates(row) for row in self.database[COLLECTIONS["logs"]].aggregate(pipeline)]

    def attack_timeline(self, *, tenant_id: str, hours: int = 24) -> list[dict[str, Any]]:
        """Aggregate alert, incident, and log activity into timeline buckets."""
        since = datetime.now(UTC) - timedelta(hours=hours)
        pipeline = [
            {"$match": {"tenant_id": tenant_id, "deleted_at": None, "observed_at": {"$gte": since}}},
            {
                "$group": {
                    "_id": {
                        "hour": {"$dateTrunc": {"date": "$observed_at", "unit": "hour"}},
                        "severity": "$severity",
                    },
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id.hour": 1}},
            {
                "$project": {
                    "_id": 0,
                    "timestamp": "$_id.hour",
                    "severity": "$_id.severity",
                    "count": 1,
                }
            },
        ]
        return [self._serialize_dates(row) for row in self.database[COLLECTIONS["logs"]].aggregate(pipeline)]

    def threat_map(self, *, tenant_id: str, limit: int = 25) -> dict[str, Any]:
        """Build map-ready threat source and indicator aggregation."""
        pipeline = [
            {"$match": {"tenant_id": tenant_id, "deleted_at": None, "status": {"$in": ["active", "watchlisted"]}}},
            {
                "$facet": {
                    "indicators": [
                        {"$sort": {"confidence": -1, "updated_at": -1}},
                        {"$limit": limit},
                        {
                            "$project": {
                                "_id": 0,
                                "indicator": 1,
                                "indicator_type": 1,
                                "source": 1,
                                "severity": 1,
                                "confidence": 1,
                                "tlp": 1,
                                "mitre_attack": 1,
                                "related_assets": 1,
                            }
                        },
                    ],
                    "by_type": [{"$group": {"_id": "$indicator_type", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}],
                    "by_source": [{"$group": {"_id": "$source", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}],
                }
            },
        ]
        row = next(iter(self.database[COLLECTIONS["threat_intelligence"]].aggregate(pipeline)), {})
        return {
            "indicators": row.get("indicators", []),
            "by_type": self._group_rows(row.get("by_type", [])),
            "by_source": self._group_rows(row.get("by_source", [])),
        }

    def _risk_level(self, score: float) -> str:
        if score >= 80:
            return "critical"
        if score >= 60:
            return "high"
        if score >= 35:
            return "medium"
        return "low"

    def _facet_count(self, row: dict, key: str) -> int:
        values = row.get(key, [])
        return int(values[0]["count"]) if values else 0

    def _group_rows(self, rows: list[dict]) -> list[dict]:
        return [{"label": row.get("_id") or "unknown", "count": row.get("count", 0)} for row in rows]

    def _serialize_dates(self, document: dict) -> dict:
        for key, value in list(document.items()):
            if isinstance(value, datetime):
                document[key] = value.isoformat()
        return document
