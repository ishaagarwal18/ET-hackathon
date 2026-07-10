"""Testing settings for SentinelAI."""

from .base import *  # noqa: F403


DEBUG = False
SECRET_KEY = "sentinelai-testing-secret-with-more-than-thirty-two-bytes"
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
