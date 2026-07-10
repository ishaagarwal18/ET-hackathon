"""Dashboard application service."""

from apps.dashboard.repositories.mongodb_repository import DashboardMongoRepository


class DashboardService:
    """Compose dashboard aggregation responses."""

    def __init__(self, repository: DashboardMongoRepository | None = None):
        self.repository = repository or DashboardMongoRepository()

    def overview(self, *, tenant_id: str) -> dict:
        """Return primary dashboard card data."""
        return {
            "active_alerts": self.repository.active_alerts(tenant_id=tenant_id),
            "risk_score": self.repository.risk_score(tenant_id=tenant_id),
            "assets": self.repository.assets(tenant_id=tenant_id),
            "incidents": self.repository.incidents(tenant_id=tenant_id),
        }

    def top_vulnerabilities(self, *, tenant_id: str, limit: int) -> list[dict]:
        return self.repository.top_vulnerabilities(tenant_id=tenant_id, limit=limit)

    def recent_logs(self, *, tenant_id: str, limit: int) -> list[dict]:
        return self.repository.recent_logs(tenant_id=tenant_id, limit=limit)

    def attack_timeline(self, *, tenant_id: str, hours: int) -> list[dict]:
        return self.repository.attack_timeline(tenant_id=tenant_id, hours=hours)

    def threat_map(self, *, tenant_id: str, limit: int) -> dict:
        return self.repository.threat_map(tenant_id=tenant_id, limit=limit)
