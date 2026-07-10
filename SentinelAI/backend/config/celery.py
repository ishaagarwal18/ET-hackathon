"""Celery application bootstrap for SentinelAI background workers."""

import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery("sentinelai")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
