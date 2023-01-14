from django.db import models
from django.contrib.auth.models import AbstractUser
from argon2 import PasswordHasher
from phonenumber_field.modelfields import PhoneNumberField
from django.core.mail import send_mail


"""This module manages generic models required for users & authentication

The following models are present here:

    - Auth: Base user login table (stores first_name, last_name, username, email, password, etc...)
    - Customer: Model storing basic user information
    - Admin: Model used for admins. Can do account creation, overall administration, etc.
"""


class Auth(AbstractUser):
    class Meta:
        verbose_name = 'Basic user auth model'
        verbose_name_plural = 'Basic user auth models'
        ordering = ['email']

    REQUIRED_FIELDS = ['email', 'password']

    USER_TYPE_CHOICES = (
        (1, 'customer'),
        (2, 'admin'),
    )

    id = models.AutoField(primary_key=True)
    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, editable=False)
    password = models.CharField(max_length=128)
    phone_number = PhoneNumberField(null=True, blank=True)

    # account confirmation / password reset stuff
    # TODO: have a different token for password reset & account confirmation
    tmp_token = models.CharField(max_length=32, null=True, default=None)
    is_disabled = models.BooleanField(default=True)

    def set_password(self, raw_password: str | None = None):
        if not raw_password:
            return
        hashed = PasswordHasher().hash(raw_password)
        self.password = hashed

    def check_password(self, raw_password=None) -> bool:
        return PasswordHasher().verify(self.password, raw_password) if raw_password else False

    def send_confirm_email(self) -> int:
        url = f'https://arkultur.creative-rift.com/confirm?token={self.tmp_token}'
        return send_mail(
            f'Welcome {self.first_name} !',
            f'Hello and welcome!\nPlease click on the following link to confirm your account:{url}',
            'noreply@arkultur.creative-rift.com',
            [self.email],
            fail_silently=False,
        )

    def send_reset_password_email(self) -> int:
        url = f'https://arkultur.creative-rift.com/reset?token={self.tmp_token}'
        return send_mail(
            f'{self.first_name}, reset your password',
            f'Please click on the following link to reset your password:{url}',
            'noreply@arkultur.creative-rift.com',
            [self.email],
            fail_silently=False,
        )

    def save(self, *args, **kwargs) -> None:
        if self.pk is None:
            self.send_confirm_email()
        return super().save(*args, **kwargs)


class Admin(models.Model):
    class Meta:
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'
        ordering = ['creation_date']

    id = models.AutoField(primary_key=True)
    auth = models.OneToOneField(Auth, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True, editable=False)


class Customer(models.Model):
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['creation_date']

    id = models.AutoField(primary_key=True)
    auth = models.OneToOneField(Auth, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True, editable=False)
