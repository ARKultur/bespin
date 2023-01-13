from django.test import TransactionTestCase
from rest_framework.response import Response
from rest_framework.test import  APIClient

from api.tests.helpers import create_random_customer, random_user_password, login_as


class DomainCRUDTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.user = create_random_customer()
        self.client: APIClient = APIClient()
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
        resp: Response = self.client.post('/address', format='json', data=creation_data)
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
        resp: Response = self.client.post('/address', format='json', data=creation_data)
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




