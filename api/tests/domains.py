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


class DomainCRUDTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.user = create_random_customer()
        self.client = APIClient()
        self.auth_token = login_as(self.user.auth.email, random_user_password())
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.auth_token}')

    def tearDown(self) -> None:
        self.user.delete()

    def test_create_an_address(self):
        creation_data = {
            'country': 'France',
            'country_code': 'FR',
            'postcode': '75007',
            'state': 'Seine',
            'state_district': 'whatever',
            'city': 'Paris',
            'street': '5 Av. Anatole France'
        }
        resp = self.client.post('/address', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)


    def test_update_an_address(self):
        creation_data = {
            'country': 'France',
            'country_code': 'FR',
            'postcode': '75007',
            'state': 'Seine',
            'state_district': 'whatever',
            'city': 'Paris',
            'street': '5 Av. Anatole France'
        }
        resp = self.client.post('/address', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)

        id = resp.data['id']
        update_data = {
            'country': 'France',
            'country_code': 'FR',
            'postcode': '75007',
            'state': 'Seine',
            'state_district': 'cool stuff',
            'city': 'Paris',
            'street': '5 Av. Anatole France'
        }
        resp = self.client.patch(f'/address/{id}', format='json', data=update_data)
        self.assertEqual(resp.status_code, 200)

    def test_delete_an_address(self):
        creation_data = {
            'country': 'France',
            'country_code': 'FR',
            'postcode': '75007',
            'state': 'Seine',
            'state_district': 'whatever',
            'city': 'Paris',
            'street': '5 Av. Anatole France'
        }
        resp = self.client.post('/address', format='json', data=creation_data)
        self.assertEqual(resp.status_code, 201)

        id = resp.data['id']
        resp = self.client.delete(f'/address/{id}', format='json')
        self.assertEqual(resp.status_code, 204)




