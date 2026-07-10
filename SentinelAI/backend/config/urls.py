"""Root URL configuration for SentinelAI."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenVerifyView


api_v1_patterns = [
    path("health/", include("core.health.urls")),
    path("auth/", include("apps.authentication.urls")),
    path("users/", include("apps.users.urls")),
    path("logs/", include("apps.logs.urls")),
    path("alerts/", include("apps.alerts.urls")),
    path("incidents/", include("apps.incidents.urls")),
    path("reports/", include("apps.reports.urls")),
    path("assets/", include("apps.assets.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("", include("apps.soc_assistant.urls")),
    path("", include("apps.attack_prediction.urls")),
    path("", include("apps.threat_intelligence.urls")),
    path("", include("apps.behavior.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1_patterns)),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
