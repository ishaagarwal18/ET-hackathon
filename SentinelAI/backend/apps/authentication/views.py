"""API views for authentication."""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.views import APIView

from apps.authentication.serializers import (
    JWTLoginSerializer,
    JWTRefreshSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserIdentitySerializer,
)
from core.responses import success_response


User = get_user_model()
security_logger = logging.getLogger("sentinelai.security")


class RegisterView(APIView):
    """Register a non-admin SentinelAI account."""

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    @extend_schema(request=RegisterSerializer, responses=UserIdentitySerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        security_logger.info("user_registered user_id=%s role=%s", user.id, user.role)
        return success_response(
            data=UserIdentitySerializer(user).data,
            message="User registered successfully.",
            http_status=status.HTTP_201_CREATED,
        )


class JWTLoginView(APIView):
    """Authenticate a user and return JWT tokens."""

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    @extend_schema(request=JWTLoginSerializer, responses=JWTLoginSerializer)
    def post(self, request):
        serializer = JWTLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        security_logger.info("jwt_login_success user_id=%s role=%s", user.id, user.role)
        return success_response(data=serializer.validated_data, message="Login successful.")


class JWTRefreshView(APIView):
    """Refresh a JWT access token."""

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    @extend_schema(request=JWTRefreshSerializer, responses=JWTRefreshSerializer)
    def post(self, request):
        serializer = JWTRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response(data=serializer.validated_data, message="Token refreshed successfully.")


class PasswordResetRequestView(APIView):
    """Generate password reset token metadata for secure delivery."""

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    @extend_schema(request=PasswordResetRequestSerializer, responses=PasswordResetRequestSerializer)
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].lower()
        user = User.objects.filter(email__iexact=email, is_active=True).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_PASSWORD_RESET_URL}?uid={uid}&token={token}"
            send_mail(
                subject="SentinelAI password reset",
                message=f"Use this secure link to reset your SentinelAI password: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
            security_logger.info("password_reset_requested user_id=%s", user.id)

        return success_response(
            data=None,
            message="If the account exists, password reset instructions have been prepared.",
        )


class PasswordResetConfirmView(APIView):
    """Set a new password using a valid password reset token."""

    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    @extend_schema(request=PasswordResetConfirmSerializer, responses=UserIdentitySerializer)
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        security_logger.info("password_reset_completed user_id=%s", user.id)
        return success_response(data=UserIdentitySerializer(user).data, message="Password reset completed successfully.")


class MeView(APIView):
    """Return the current authenticated user's identity and role."""

    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(responses=UserIdentitySerializer)
    def get(self, request):
        return success_response(data=UserIdentitySerializer(request.user).data, message="Authenticated user loaded.")
