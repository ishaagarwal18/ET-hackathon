"""API views for users."""

from rest_framework import permissions, viewsets

from apps.users.models import User
from apps.users.serializers import UserSerializer
from core.permissions.roles import HasPlatformRole, PlatformRole


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only user endpoints for authenticated API clients."""

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, HasPlatformRole)
    allowed_roles = (
        PlatformRole.SECURITY_ADMIN,
        PlatformRole.GOVERNMENT_OFFICER,
        PlatformRole.READ_ONLY_AUDITOR,
    )
