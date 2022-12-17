import os
import logging

from django.conf import settings
from django.db import transaction
from django.db.transaction import TransactionManagementError
from django.test import TransactionTestCase, TestCase
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient

from api.tests.helpers import create_random_customer, create_random_admin, random_user_password, login_as


class AuthTestCase(TransactionTestCase):

    """
        Tests if accounts can be logged in (admin or customer) and logged out
        also tests for wrong password
    """

    def setUp(self) -> None:
        self.user = create_random_customer()
        self.admin = create_random_admin()

    def tearDown(self) -> None:
        self.user.delete()
        self.admin.delete()

    def test_can_login_customer_account(self) -> None:
        client = APIClient()
        auth_token = login_as(self.user.auth.email, random_user_password())
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
        response = client.get(f'/ping')
        self.assertEqual(response.status_code, 200)

    def test_can_login_admin_account(self) -> None:
        client = APIClient()
        auth_token = login_as(self.admin.auth.email, random_user_password())
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')

    def test_can_logout_account(self) -> None:
        client = APIClient()
        auth_token = login_as(self.admin.auth.email, random_user_password())
        client.credentials(HTTP_AUTHORIZATION=f'Token {auth_token}')
        response = client.get(f'/logout')
        self.assertEqual(response.status_code, 200)

    def test_unknown_account(self) -> None:
        client = APIClient()
        response = client.post('/login', format='json', data={'email': 'email@email.com', 'password': '1234'})
        self.assertEqual(response.status_code, 404)

    def test_wrong_password(self) -> None:
        client = APIClient()
        response = client.post('/login', format='json', data={'email': self.admin.auth.email, 'password': '1234'})
        self.assertEqual(response.status_code, 403)
