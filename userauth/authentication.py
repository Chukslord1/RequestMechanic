from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class PinOrPasswordAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, pin=None, **kwargs):
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        elif user.check_pin(pin):
            return user

        return None
