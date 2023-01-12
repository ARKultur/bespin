"""This module stores the authentication backend"""

import argon2.exceptions
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    """Basic email backend (authenticate with email and password)"""

    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user_by_email(self, email):
        model = get_user_model()
        return model.objects.filter(email=email).first()

    def get_user(self, user_id):
        model = get_user_model()
        return model.objects.filter(pk=user_id).first()

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = self.get_user_by_email(email=username)
            return user if user and user.check_password(password) else None
        except argon2.exceptions.VerifyMismatchError:
            return None
