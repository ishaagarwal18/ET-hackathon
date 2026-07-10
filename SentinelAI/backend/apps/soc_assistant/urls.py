"""URL routes for AI SOC Assistant APIs."""

from django.urls import path

from apps.soc_assistant.views import SOCAssistantChatView, SOCAssistantHistoryView, SOCAssistantStreamView


app_name = "soc_assistant"

urlpatterns = [
    path("soc-assistant/chat/", SOCAssistantChatView.as_view(), name="chat"),
    path("soc-assistant/chat/stream/", SOCAssistantStreamView.as_view(), name="chat-stream"),
    path("soc-assistant/history/", SOCAssistantHistoryView.as_view(), name="history"),
]
