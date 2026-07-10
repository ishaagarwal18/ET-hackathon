"""URL routes for reports."""

from django.urls import path

from apps.reports.views import DownloadReportView, GenerateIncidentReportView


app_name = "reports"

urlpatterns = [
    path("generate-incident-report/", GenerateIncidentReportView.as_view(), name="generate-incident-report"),
    path("download/<str:filename>/", DownloadReportView.as_view(), name="download-report"),
]
