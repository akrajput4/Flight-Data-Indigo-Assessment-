# permissions.py

from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.conf import settings


class Permission(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Authorization', '').split(' ')[1]
        if not token:
            return False

        try:
            validated_token = self.get_validated_token(token)
            secret_key = validated_token.get('secret_key')
            return secret_key == settings.SECRET_KEY_FOR_TOKEN
        except InvalidToken:
            return False

    def get_validated_token(self, raw_token):
        validated_token = JWTAuthentication().get_validated_token(raw_token)
        self.validate_token(validated_token)
        return validated_token

    def validate_token(self, token):
        # Check if the secret key matches
        if token.get('secret_key') != settings.SECRET_KEY_FOR_TOKEN:
            raise InvalidToken("Invalid Token")
