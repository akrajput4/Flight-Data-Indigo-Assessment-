from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

from UserManagement.models import User


def create_jwt_token(email):
    try:
        user = User.objects.get(email_id=email)
    except User.DoesNotExist:
        raise AuthenticationFailed('No user found with this email address')

    refresh = RefreshToken.for_user(user)

    # Add custom claims
    refresh['role'] = 'user'  # Assuming you have a role field in your User model
    refresh['secret_key'] = settings.SECRET_KEY_FOR_TOKEN

    # Manually set the expiration time for the access token to 2 hours
    refresh.access_token.set_exp(lifetime=timedelta(hours=2))

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
