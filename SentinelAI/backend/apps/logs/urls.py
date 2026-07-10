"""URL routes for logs."""

from django.urls import path

from apps.logs.views import ListLogsView, LogDetailsView, UploadLogView


app_name = "logs"

urlpatterns = [
    path("upload-log/", UploadLogView.as_view(), name="upload-log"),
    path("list-logs/", ListLogsView.as_view(), name="list-logs"),
    path("log-details/", LogDetailsView.as_view(), name="log-details"),
]
