"""MongoDB JSON Schema validators for SentinelAI collections."""

from database.mongodb.common import (
    AUDIT_FIELDS,
    CONFIDENCE,
    METADATA,
    OBJECT_ID_REF,
    SEVERITY,
    STATUS,
    TAGS,
    TENANT_ID,
    TIMESTAMPS,
)
from database.mongodb.collections import COLLECTIONS


def collection_validator(required: list[str], properties: dict) -> dict:
    """Build a MongoDB collection validator."""
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "required": required,
            "additionalProperties": True,
            "properties": {
                **TENANT_ID,
                **TIMESTAMPS,
                **STATUS,
                **METADATA,
                **AUDIT_FIELDS,
                **properties,
            },
        }
    }


COLLECTION_SCHEMAS = {
    COLLECTIONS["users"]: collection_validator(
        required=["tenant_id", "email", "username", "roles", "status", "created_at", "updated_at", "metadata"],
        properties={
            "email": {"bsonType": "string", "pattern": r"^[^@\s]+@[^@\s]+\.[^@\s]+$"},
            "username": {"bsonType": "string", "minLength": 3, "maxLength": 150},
            "full_name": {"bsonType": "string", "maxLength": 255},
            "password_hash": {"bsonType": "string"},
            "roles": {"bsonType": "array", "items": {"bsonType": "string"}, "minItems": 1},
            "permissions": {"bsonType": "array", "items": {"bsonType": "string"}, "uniqueItems": True},
            "mfa_enabled": {"bsonType": "bool"},
            "last_login_at": {"bsonType": ["date", "null"]},
            "profile": {
                "bsonType": "object",
                "properties": {
                    "department": {"bsonType": "string"},
                    "job_title": {"bsonType": "string"},
                    "timezone": {"bsonType": "string"},
                },
            },
        },
    ),
    COLLECTIONS["assets"]: collection_validator(
        required=["tenant_id", "asset_key", "name", "asset_type", "criticality", "status", "created_at", "updated_at", "metadata"],
        properties={
            "asset_key": {"bsonType": "string", "minLength": 1},
            "name": {"bsonType": "string", "minLength": 1, "maxLength": 255},
            "asset_type": {"bsonType": "string", "enum": ["endpoint", "server", "cloud", "network", "identity", "application", "database", "container", "other"]},
            "criticality": {"bsonType": "string", "enum": ["low", "medium", "high", "critical"]},
            "owner": OBJECT_ID_REF,
            "ip_addresses": {"bsonType": "array", "items": {"bsonType": "string"}},
            "hostnames": {"bsonType": "array", "items": {"bsonType": "string"}},
            "environment": {"bsonType": "string", "enum": ["production", "staging", "development", "testing", "sandbox", "unknown"]},
            "tags": TAGS,
            "risk_score": {"bsonType": "int", "minimum": 0, "maximum": 100},
            "last_seen_at": {"bsonType": ["date", "null"]},
            "relationships": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["type", "target"],
                    "properties": {
                        "type": {"bsonType": "string", "enum": ["depends_on", "communicates_with", "owned_by", "hosts", "protects"]},
                        "target": OBJECT_ID_REF,
                    },
                },
            },
        },
    ),
    COLLECTIONS["logs"]: collection_validator(
        required=["tenant_id", "event_id", "source", "event_type", "severity", "status", "observed_at", "created_at", "updated_at", "metadata"],
        properties={
            "event_id": {"bsonType": "string", "minLength": 1},
            "source": {"bsonType": "string", "minLength": 1},
            "event_type": {"bsonType": "string", "minLength": 1},
            "severity": SEVERITY,
            "message": {"bsonType": "string"},
            "observed_at": {"bsonType": "date"},
            "asset": OBJECT_ID_REF,
            "user": OBJECT_ID_REF,
            "raw": {"bsonType": "object"},
            "normalized": {"bsonType": "object"},
            "correlation": {
                "bsonType": "object",
                "properties": {
                    "trace_id": {"bsonType": "string"},
                    "session_id": {"bsonType": "string"},
                    "parent_event_id": {"bsonType": "string"},
                },
            },
        },
    ),
    COLLECTIONS["alerts"]: collection_validator(
        required=["tenant_id", "alert_key", "title", "severity", "status", "confidence", "created_at", "updated_at", "metadata"],
        properties={
            "alert_key": {"bsonType": "string", "minLength": 1},
            "title": {"bsonType": "string", "minLength": 1, "maxLength": 300},
            "description": {"bsonType": "string"},
            "severity": SEVERITY,
            "status": {"bsonType": "string", "enum": ["new", "triaged", "investigating", "suppressed", "resolved", "false_positive", "archived"]},
            "confidence": CONFIDENCE,
            "source": {"bsonType": "string"},
            "rule_id": {"bsonType": "string"},
            "assets": {"bsonType": "array", "items": OBJECT_ID_REF},
            "users": {"bsonType": "array", "items": OBJECT_ID_REF},
            "logs": {"bsonType": "array", "items": OBJECT_ID_REF},
            "incident": OBJECT_ID_REF,
            "first_seen_at": {"bsonType": "date"},
            "last_seen_at": {"bsonType": "date"},
            "tags": TAGS,
        },
    ),
    COLLECTIONS["incidents"]: collection_validator(
        required=["tenant_id", "incident_key", "title", "severity", "status", "created_at", "updated_at", "metadata"],
        properties={
            "incident_key": {"bsonType": "string", "minLength": 1},
            "title": {"bsonType": "string", "minLength": 1, "maxLength": 300},
            "summary": {"bsonType": "string"},
            "severity": SEVERITY,
            "status": {"bsonType": "string", "enum": ["open", "triage", "containment", "eradication", "recovery", "closed", "archived"]},
            "priority": {"bsonType": "string", "enum": ["p1", "p2", "p3", "p4"]},
            "owner": OBJECT_ID_REF,
            "alerts": {"bsonType": "array", "items": OBJECT_ID_REF},
            "assets": {"bsonType": "array", "items": OBJECT_ID_REF},
            "users": {"bsonType": "array", "items": OBJECT_ID_REF},
            "timeline": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["timestamp", "event_type", "description"],
                    "properties": {
                        "timestamp": {"bsonType": "date"},
                        "event_type": {"bsonType": "string"},
                        "description": {"bsonType": "string"},
                        "actor": OBJECT_ID_REF,
                    },
                },
            },
            "opened_at": {"bsonType": "date"},
            "closed_at": {"bsonType": ["date", "null"]},
            "tags": TAGS,
        },
    ),
    COLLECTIONS["threat_intelligence"]: collection_validator(
        required=["tenant_id", "indicator", "indicator_type", "source", "confidence", "status", "created_at", "updated_at", "metadata"],
        properties={
            "indicator": {"bsonType": "string", "minLength": 1},
            "indicator_type": {"bsonType": "string", "enum": ["ip", "domain", "url", "hash", "email", "mutex", "cve", "ttp", "identity", "other"]},
            "source": {"bsonType": "string", "minLength": 1},
            "confidence": CONFIDENCE,
            "severity": SEVERITY,
            "status": {"bsonType": "string", "enum": ["active", "expired", "revoked", "watchlisted", "archived"]},
            "tlp": {"bsonType": "string", "enum": ["white", "green", "amber", "red"]},
            "valid_from": {"bsonType": "date"},
            "valid_until": {"bsonType": ["date", "null"]},
            "related_cves": {"bsonType": "array", "items": OBJECT_ID_REF},
            "related_assets": {"bsonType": "array", "items": OBJECT_ID_REF},
            "related_alerts": {"bsonType": "array", "items": OBJECT_ID_REF},
            "mitre_attack": {"bsonType": "array", "items": {"bsonType": "string"}},
            "tags": TAGS,
        },
    ),
    COLLECTIONS["cve"]: collection_validator(
        required=["tenant_id", "cve_id", "title", "severity", "status", "published_at", "created_at", "updated_at", "metadata"],
        properties={
            "cve_id": {"bsonType": "string", "pattern": r"^CVE-\d{4}-\d{4,}$"},
            "title": {"bsonType": "string", "minLength": 1, "maxLength": 300},
            "description": {"bsonType": "string"},
            "severity": SEVERITY,
            "status": {"bsonType": "string", "enum": ["new", "under_review", "exploitable", "mitigated", "accepted", "archived"]},
            "cvss": {
                "bsonType": "object",
                "properties": {
                    "version": {"bsonType": "string"},
                    "score": {"bsonType": "double", "minimum": 0, "maximum": 10},
                    "vector": {"bsonType": "string"},
                },
            },
            "cwe": {"bsonType": "array", "items": {"bsonType": "string"}},
            "affected_assets": {"bsonType": "array", "items": OBJECT_ID_REF},
            "references": {"bsonType": "array", "items": {"bsonType": "string"}},
            "published_at": {"bsonType": "date"},
            "modified_at": {"bsonType": ["date", "null"]},
            "exploitation": {
                "bsonType": "object",
                "properties": {
                    "known_exploited": {"bsonType": "bool"},
                    "exploit_maturity": {"bsonType": "string"},
                    "epss_score": {"bsonType": ["double", "null"], "minimum": 0, "maximum": 1},
                },
            },
            "tags": TAGS,
        },
    ),
    COLLECTIONS["behavior_profiles"]: collection_validator(
        required=["tenant_id", "profile_key", "subject_type", "subject", "status", "created_at", "updated_at", "metadata"],
        properties={
            "profile_key": {"bsonType": "string", "minLength": 1},
            "subject_type": {"bsonType": "string", "enum": ["user", "asset", "service_account", "application", "network_segment"]},
            "subject": OBJECT_ID_REF,
            "status": {"bsonType": "string", "enum": ["learning", "active", "stale", "suspended", "archived"]},
            "baseline_window_days": {"bsonType": "int", "minimum": 1, "maximum": 365},
            "risk_score": {"bsonType": "int", "minimum": 0, "maximum": 100},
            "features": {"bsonType": "object"},
            "statistics": {"bsonType": "object"},
            "last_trained_at": {"bsonType": ["date", "null"]},
            "related_alerts": {"bsonType": "array", "items": OBJECT_ID_REF},
            "tags": TAGS,
        },
    ),
    COLLECTIONS["reports"]: collection_validator(
        required=["tenant_id", "report_key", "title", "report_type", "status", "created_at", "updated_at", "metadata"],
        properties={
            "report_key": {"bsonType": "string", "minLength": 1},
            "title": {"bsonType": "string", "minLength": 1, "maxLength": 300},
            "report_type": {"bsonType": "string", "enum": ["executive", "incident", "compliance", "asset", "risk", "threat_intelligence", "custom"]},
            "status": {"bsonType": "string", "enum": ["draft", "generating", "ready", "failed", "archived"]},
            "requested_by": OBJECT_ID_REF,
            "scope": {
                "bsonType": "object",
                "properties": {
                    "assets": {"bsonType": "array", "items": OBJECT_ID_REF},
                    "incidents": {"bsonType": "array", "items": OBJECT_ID_REF},
                    "alerts": {"bsonType": "array", "items": OBJECT_ID_REF},
                    "time_range": {
                        "bsonType": "object",
                        "properties": {
                            "start": {"bsonType": "date"},
                            "end": {"bsonType": "date"},
                        },
                    },
                },
            },
            "storage": {
                "bsonType": "object",
                "properties": {
                    "provider": {"bsonType": "string"},
                    "uri": {"bsonType": "string"},
                    "checksum": {"bsonType": "string"},
                    "content_type": {"bsonType": "string"},
                },
            },
            "generated_at": {"bsonType": ["date", "null"]},
            "expires_at": {"bsonType": ["date", "null"]},
            "tags": TAGS,
        },
    ),
}
