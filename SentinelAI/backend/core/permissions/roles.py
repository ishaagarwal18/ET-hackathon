"""Role-based permission classes for SentinelAI APIs."""

from rest_framework.permissions import BasePermission


class PlatformRole:
    """Canonical SentinelAI platform roles."""

    SOC_ANALYST = "soc_analyst"
    SECURITY_ADMIN = "security_admin"
    GOVERNMENT_OFFICER = "government_officer"
    READ_ONLY_AUDITOR = "read_only_auditor"

    ALL = (
        SOC_ANALYST,
        SECURITY_ADMIN,
        GOVERNMENT_OFFICER,
        READ_ONLY_AUDITOR,
    )


class IsAuthenticatedAndActive(BasePermission):
    """Allow only authenticated active users."""

    message = "Authentication credentials were not provided or the account is inactive."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)


class HasPlatformRole(BasePermission):
    """Base role permission that checks a view's allowed_roles attribute."""

    message = "You do not have permission to access this resource."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or not request.user.is_active:
            return False

        allowed_roles = getattr(view, "allowed_roles", PlatformRole.ALL)
        return request.user.role in allowed_roles or request.user.is_superuser


class IsSecurityAdmin(BasePermission):
    """Allow only security administrators or superusers."""

    message = "Security administrator role is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and (request.user.is_superuser or request.user.role == PlatformRole.SECURITY_ADMIN)
        )


class IsReadOnlyRole(BasePermission):
    """Allow safe methods for any authenticated SentinelAI role."""

    message = "Read-only access is required."

    def has_permission(self, request, view):
        return bool(
            request.method in ("GET", "HEAD", "OPTIONS")
            and request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.role in PlatformRole.ALL
        )
