import os
import logging
from datetime import datetime

from faker import Faker

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


class RegisterTestCase(TransactionTestCase):
    """
        Tests account registration feature
    """

    def test_can_register_new_customer(self) -> None:
        client = APIClient()
        fake = Faker()

        name = fake.name()
        registration_settings = {
          "auth": {
            "username": name.split(' ')[0],
            "email": fake.email(),
            "first_name": name.split(' ')[0],
            "last_name": name.split(' ')[1],
            "password": random_user_password()
          },
          "creation_date": "2022-12-17T21:36:37.402Z"
        }
        response = client.post('/register', format='json', data=registration_settings)
        self.assertEqual(response.status_code, 201)

    def test_invalid_data(self) -> None:
        client = APIClient()
        registration_settings = {
                'first_name': 'kendrick',
                }
        response = client.post('/register', format='json', data=registration_settings)
        self.assertEqual(response.status_code, 400)


class CrudCustomerTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.admin = create_random_admin()
        self.client = APIClient()
        self.auth_token = login_as(self.admin.auth.email, random_user_password())
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.auth_token}')

    def tearDown(self) -> None:
        response = self.client.get(f'/logout')
        self.assertEqual(response.status_code, 200)
        self.admin.delete()

    def test_create_a_customer(self):
        fake = Faker()
        name = fake.name()
        creation_data = {
          "auth": {
            "username": name.split(' ')[0],
            "email": fake.email(),
            "first_name": name.split(' ')[0],
            "last_name": name.split(' ')[1],
            "password": random_user_password()
          },
          "creation_date": "2022-12-17T21:36:37.402Z"
        }
        resp = self.client.post('/customer', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)


    def test_update_a_customer(self):
        fake = Faker()
        name = fake.name()
        creation_data = {
          "auth": {
            "username": name.split(' ')[0],
            "email": fake.email(),
            "first_name": name.split(' ')[0],
            "last_name": name.split(' ')[1],
            "password": random_user_password()
          },
          "creation_date": "2022-12-17T21:36:37.402Z"
        }
        resp = self.client.post('/customer', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)
        name = fake.name()
        update_data = {
            "auth": {
                "username": name.split(' ')[0],
                "email": fake.email(),
                "first_name": name.split(' ')[0],
                "last_name": name.split(' ')[1],
                "role": 1,
                "password": random_user_password()
          },
          "creation_date": "2022-12-17T21:36:37.402Z"
        }

        id = resp.data["id"]
        resp = self.client.get(f'/customer/{id}', format='json')
        self.assertEqual(resp.status_code, 200)

        resp = self.client.patch(f'/customer/{id}', format='json', data=update_data)
        self.assertEqual(resp.status_code, 200)

    def test_delete_a_customer(self):
        fake = Faker()
        name = fake.name()
        creation_data = {
          "auth": {
            "username": name.split(' ')[0],
            "email": fake.email(),
            "first_name": name.split(' ')[0],
            "last_name": name.split(' ')[1],
            "password": random_user_password()
          },
          "creation_date": "2022-12-17T21:36:37.402Z"
        }
        resp = self.client.post('/customer', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)

        id = resp.data["id"]
        resp = self.client.delete(f'/customer/{id}', format='json')
        self.assertEqual(resp.status_code, 204)


class AddressCRUDTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.user = create_random_customer()
        self.client = APIClient()
        self.auth_token = login_as(self.user.auth.email, random_user_password())
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.auth_token}')

    def tearDown(self) -> None:
        self.user.delete()

    def test_create_an_address(self):
        creation_data = {
            'owner': self.user.id,
            'country': 'France',
            'country_code': 'FR',
            'postcode': '75007',
            'state': 'Seine',
            'state_district': 'whatever',
            'city': 'Paris',
            'street': 'Av. Anatole France',
            'street_number': 5
        }
        resp = self.client.post('/address', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)


    def test_update_an_address(self):
        creation_data = {
            'owner': self.user.id,
            'country': 'France',
            'country_code': 'FR',
            'postcode': '75007',
            'state': 'Seine',
            'state_district': 'whatever',
            'city': 'Paris',
            'street': 'Av. Anatole France',
            'street_number': 5

        }
        resp = self.client.post('/address', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)

        id = resp.data['id']
        update_data = {
            'owner': self.user.id,
            'country': 'France',
            'country_code': 'FR',
            'postcode': '75007',
            'state': 'Seine',
            'state_district': 'cool stuff',
            'city': 'Paris',
            'street': 'Av. Anatole France',
            'street_number': 5
        }
        resp = self.client.patch(f'/address/{id}', format='json', data=update_data)
        self.assertEqual(resp.status_code, 200)

    def test_delete_an_address(self):
        creation_data = {
            'owner': self.user.id,
            'country': 'France',
            'country_code': 'FR',
            'postcode': '75007',
            'state': 'Seine',
            'state_district': 'whatever',
            'city': 'Paris',
            'street': 'Av. Anatole France',
            'street_number': 5
        }
        resp = self.client.post('/address', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)

        id = resp.data['id']
        resp = self.client.delete(f'/address/{id}', format='json')
        self.assertEqual(resp.status_code, 204)

class NodeCrudTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.user = create_random_customer()
        self.client = APIClient()
        self.auth_token = login_as(self.user.auth.email, random_user_password())
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.auth_token}')
        creation_data = {
            'owner': self.user.id,
            'country': 'France',
            'country_code': 'FR',
            'postcode': '75007',
            'state': 'Seine',
            'state_district': 'whatever',
            'city': 'Paris',
            'street': 'Av. Anatole France',
            'street_number': 5
        }
        resp = self.client.post('/address', format='json', data=creation_data)
        self.addr_id = resp.data['id']

    def tearDown(self) -> None:
        self.user.delete()

    def test_create_a_node(self):
        creation_data = {
            'address': self.addr_id,
            'name': 'eiffel tower',
            'latitude': 48.8584,
            'longitude': 2.2945
        }
        resp = self.client.post('/node', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)

    def test_update_a_node(self):
        creation_data = {
            'address': self.addr_id,
            'name': 'eiffel tower',
            'latitude': 48.8584,
            'longitude': 2.2945
        }
        resp = self.client.post('/node', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)

        id = resp.data['id']
        update_data = {
            'address': self.addr_id,
            'name': 'eiffel tower',
            'longitude': 48.8584,
            'latitude': 2.2945
        }
        resp = self.client.patch(f'/node/{id}', format='json', data=update_data)
        self.assertEqual(resp.status_code, 200)

    def test_delete_a_node(self):
        creation_data = {
            'address': self.addr_id,
            'name': 'eiffel tower',
            'latitude': 48.8584,
            'longitude': 2.2945
        }
        resp = self.client.post('/node', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)
        id = resp.data['id']

        resp = self.client.delete(f'/node/{id}', format='json')
        self.assertEqual(resp.status_code, 204)
