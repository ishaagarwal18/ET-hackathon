"""MongoDB index definitions for SentinelAI collections."""

from pymongo import ASCENDING, DESCENDING, HASHED, IndexModel, TEXT

from database.mongodb.collections import COLLECTIONS


COLLECTION_INDEXES = {
    COLLECTIONS["users"]: [
        IndexModel([("tenant_id", ASCENDING), ("email", ASCENDING)], unique=True, name="uniq_tenant_email"),
        IndexModel([("tenant_id", ASCENDING), ("username", ASCENDING)], unique=True, name="uniq_tenant_username"),
        IndexModel([("tenant_id", ASCENDING), ("status", ASCENDING)], name="idx_users_status"),
        IndexModel([("roles", ASCENDING)], name="idx_users_roles"),
        IndexModel([("created_at", DESCENDING)], name="idx_users_created_at"),
    ],
    COLLECTIONS["assets"]: [
        IndexModel([("tenant_id", ASCENDING), ("asset_key", ASCENDING)], unique=True, name="uniq_tenant_asset_key"),
        IndexModel([("tenant_id", ASCENDING), ("asset_type", ASCENDING), ("status", ASCENDING)], name="idx_assets_type_status"),
        IndexModel([("tenant_id", ASCENDING), ("criticality", ASCENDING), ("risk_score", DESCENDING)], name="idx_assets_risk"),
        IndexModel([("tenant_id", ASCENDING), ("deleted_at", ASCENDING), ("risk_score", DESCENDING)], name="idx_assets_dashboard_risk"),
        IndexModel([("ip_addresses", ASCENDING)], name="idx_assets_ip_addresses"),
        IndexModel([("hostnames", ASCENDING)], name="idx_assets_hostnames"),
        IndexModel([("tags", ASCENDING)], name="idx_assets_tags"),
        IndexModel([("last_seen_at", DESCENDING)], name="idx_assets_last_seen"),
    ],
    COLLECTIONS["logs"]: [
        IndexModel([("tenant_id", ASCENDING), ("event_id", ASCENDING)], unique=True, name="uniq_tenant_event_id"),
        IndexModel([("tenant_id", ASCENDING), ("observed_at", DESCENDING)], name="idx_logs_observed_at"),
        IndexModel([("tenant_id", ASCENDING), ("deleted_at", ASCENDING), ("observed_at", DESCENDING)], name="idx_logs_dashboard_recent"),
        IndexModel([("tenant_id", ASCENDING), ("source", ASCENDING), ("event_type", ASCENDING)], name="idx_logs_source_type"),
        IndexModel([("asset.id", ASCENDING)], name="idx_logs_asset"),
        IndexModel([("user.id", ASCENDING)], name="idx_logs_user"),
        IndexModel([("message", TEXT), ("normalized.command_line", TEXT)], name="txt_logs_message_command"),
    ],
    COLLECTIONS["alerts"]: [
        IndexModel([("tenant_id", ASCENDING), ("alert_key", ASCENDING)], unique=True, name="uniq_tenant_alert_key"),
        IndexModel([("tenant_id", ASCENDING), ("status", ASCENDING), ("severity", ASCENDING)], name="idx_alerts_status_severity"),
        IndexModel([("tenant_id", ASCENDING), ("deleted_at", ASCENDING), ("status", ASCENDING), ("severity", ASCENDING)], name="idx_alerts_dashboard_active"),
        IndexModel([("tenant_id", ASCENDING), ("confidence", DESCENDING)], name="idx_alerts_confidence"),
        IndexModel([("assets.id", ASCENDING)], name="idx_alerts_assets"),
        IndexModel([("users.id", ASCENDING)], name="idx_alerts_users"),
        IndexModel([("incident.id", ASCENDING)], name="idx_alerts_incident"),
        IndexModel([("last_seen_at", DESCENDING)], name="idx_alerts_last_seen"),
        IndexModel([("title", TEXT), ("description", TEXT)], name="txt_alerts_title_description"),
    ],
    COLLECTIONS["incidents"]: [
        IndexModel([("tenant_id", ASCENDING), ("incident_key", ASCENDING)], unique=True, name="uniq_tenant_incident_key"),
        IndexModel([("tenant_id", ASCENDING), ("status", ASCENDING), ("priority", ASCENDING)], name="idx_incidents_status_priority"),
        IndexModel([("tenant_id", ASCENDING), ("deleted_at", ASCENDING), ("status", ASCENDING), ("updated_at", DESCENDING)], name="idx_incidents_dashboard_status"),
        IndexModel([("tenant_id", ASCENDING), ("severity", ASCENDING), ("opened_at", DESCENDING)], name="idx_incidents_severity_opened"),
        IndexModel([("owner.id", ASCENDING)], name="idx_incidents_owner"),
        IndexModel([("alerts.id", ASCENDING)], name="idx_incidents_alerts"),
        IndexModel([("assets.id", ASCENDING)], name="idx_incidents_assets"),
        IndexModel([("title", TEXT), ("summary", TEXT)], name="txt_incidents_title_summary"),
    ],
    COLLECTIONS["threat_intelligence"]: [
        IndexModel([("tenant_id", ASCENDING), ("indicator", ASCENDING), ("indicator_type", ASCENDING)], unique=True, name="uniq_tenant_indicator"),
        IndexModel([("tenant_id", ASCENDING), ("status", ASCENDING), ("confidence", DESCENDING)], name="idx_ti_status_confidence"),
        IndexModel([("tenant_id", ASCENDING), ("deleted_at", ASCENDING), ("status", ASCENDING), ("confidence", DESCENDING)], name="idx_ti_dashboard_map"),
        IndexModel([("indicator", HASHED)], name="hash_ti_indicator"),
        IndexModel([("related_cves.id", ASCENDING)], name="idx_ti_related_cves"),
        IndexModel([("related_assets.id", ASCENDING)], name="idx_ti_related_assets"),
        IndexModel([("valid_until", ASCENDING)], name="idx_ti_valid_until"),
        IndexModel([("tags", ASCENDING)], name="idx_ti_tags"),
    ],
    COLLECTIONS["cve"]: [
        IndexModel([("tenant_id", ASCENDING), ("cve_id", ASCENDING)], unique=True, name="uniq_tenant_cve_id"),
        IndexModel([("tenant_id", ASCENDING), ("severity", ASCENDING), ("status", ASCENDING)], name="idx_cve_severity_status"),
        IndexModel([("tenant_id", ASCENDING), ("deleted_at", ASCENDING), ("status", ASCENDING), ("published_at", DESCENDING)], name="idx_cve_dashboard_top"),
        IndexModel([("cvss.score", DESCENDING)], name="idx_cve_cvss_score"),
        IndexModel([("exploitation.known_exploited", ASCENDING), ("exploitation.epss_score", DESCENDING)], name="idx_cve_exploitation"),
        IndexModel([("affected_assets.id", ASCENDING)], name="idx_cve_affected_assets"),
        IndexModel([("published_at", DESCENDING)], name="idx_cve_published_at"),
        IndexModel([("title", TEXT), ("description", TEXT), ("cve_id", TEXT)], name="txt_cve_search"),
    ],
    COLLECTIONS["behavior_profiles"]: [
        IndexModel([("tenant_id", ASCENDING), ("profile_key", ASCENDING)], unique=True, name="uniq_tenant_profile_key"),
        IndexModel([("tenant_id", ASCENDING), ("subject_type", ASCENDING), ("subject.id", ASCENDING)], unique=True, name="uniq_behavior_subject"),
        IndexModel([("tenant_id", ASCENDING), ("status", ASCENDING), ("risk_score", DESCENDING)], name="idx_behavior_status_risk"),
        IndexModel([("tenant_id", ASCENDING), ("deleted_at", ASCENDING), ("status", ASCENDING), ("risk_score", DESCENDING)], name="idx_behavior_dashboard_risk"),
        IndexModel([("last_trained_at", DESCENDING)], name="idx_behavior_last_trained"),
        IndexModel([("related_alerts.id", ASCENDING)], name="idx_behavior_related_alerts"),
    ],
    COLLECTIONS["reports"]: [
        IndexModel([("tenant_id", ASCENDING), ("report_key", ASCENDING)], unique=True, name="uniq_tenant_report_key"),
        IndexModel([("tenant_id", ASCENDING), ("report_type", ASCENDING), ("status", ASCENDING)], name="idx_reports_type_status"),
        IndexModel([("requested_by.id", ASCENDING)], name="idx_reports_requested_by"),
        IndexModel([("generated_at", DESCENDING)], name="idx_reports_generated_at"),
        IndexModel([("expires_at", ASCENDING)], name="idx_reports_expires_at"),
        IndexModel([("title", TEXT)], name="txt_reports_title"),
    ],
}
