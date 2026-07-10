"""Serializers for authentication."""

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer


User = get_user_model()


class UserIdentitySerializer(serializers.ModelSerializer):
    """Authenticated user identity payload."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_verified",
        )
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """Register a SentinelAI user."""

    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password_confirm = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "password",
            "password_confirm",
        )

    def validate_role(self, value):
        """Restrict self-service registration to non-admin roles."""
        if value == User.Role.SECURITY_ADMIN:
            raise serializers.ValidationError("Security Admin accounts must be provisioned by an administrator.")
        return value

    def validate(self, attrs):
        """Validate password confirmation and password strength."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})

        validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        """Create a user with a hashed password."""
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class JWTLoginSerializer(TokenObtainPairSerializer):
    """Issue JWT access and refresh tokens."""

    def validate(self, attrs):
        """Authenticate active users and include identity details."""
        user = authenticate(
            request=self.context.get("request"),
            username=attrs.get(self.username_field),
            password=attrs.get("password"),
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")

        data = super().validate(attrs)
        data["user"] = UserIdentitySerializer(self.user).data
        return data

    @classmethod
    def get_token(cls, user):
        """Include role claims in generated tokens."""
        token = super().get_token(user)
        token["role"] = user.role
        token["email"] = user.email
        token["is_verified"] = user.is_verified
        return token


class JWTRefreshSerializer(TokenRefreshSerializer):
    """Refresh JWT access tokens."""


class PasswordResetRequestSerializer(serializers.Serializer):
    """Request a password reset token."""

    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Confirm password reset using uid and token."""

    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password_confirm = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        """Validate reset token and password strength."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})

        try:
            user_id = force_str(urlsafe_base64_decode(attrs["uid"]))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"token": "Invalid password reset token."}) from None

        if not default_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError({"token": "Invalid password reset token."})

        validate_password(attrs["password"], user=user)
        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        """Set the new password."""
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password"])
        user.save(update_fields=["password"])
        return user
