"""URL routes for authentication."""

from django.urls import path

from apps.authentication.views import (
    JWTLoginView,
    JWTRefreshView,
    MeView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
)


app_name = "authentication"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", JWTLoginView.as_view(), name="jwt-login"),
    path("refresh/", JWTRefreshView.as_view(), name="jwt-refresh"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("me/", MeView.as_view(), name="me"),
]
