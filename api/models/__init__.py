from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from argon2 import PasswordHasher
from phonenumber_field.modelfields import PhoneNumberField


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

    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, editable=False)
    email = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    phone_number = PhoneNumberField(null=True, blank=True)

    def set_password(self, raw_password=None):
        hashed = PasswordHasher().hash(raw_password)
        self.password = hashed

    def check_password(self, raw_password=None) -> bool:
        return PasswordHasher().verify(self.password, raw_password) if raw_password else False


class Admin(models.Model):
    class Meta:
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administrators'
        ordering = ['creation_date']

    auth = models.OneToOneField(Auth, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True, editable=False)


class Customer(models.Model):
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['creation_date']

    auth = models.OneToOneField(Auth, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True, editable=False)
