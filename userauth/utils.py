from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    try:
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    except TokenError:
        raise AuthenticationFailed(
            detail="Invalid or expired token.",
            code=403  # Set the code to 403 for authentication failure
        )
