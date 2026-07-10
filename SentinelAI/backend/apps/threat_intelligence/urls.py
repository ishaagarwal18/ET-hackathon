"""URL routes for Threat Intelligence Agent APIs."""

from django.urls import path

from apps.threat_intelligence.views import ThreatIntelChatHistoryView, ThreatIntelChatView


app_name = "threat_intelligence"

urlpatterns = [
    path("chat/", ThreatIntelChatView.as_view(), name="chat"),
    path("chat/history/", ThreatIntelChatHistoryView.as_view(), name="chat-history"),
]
