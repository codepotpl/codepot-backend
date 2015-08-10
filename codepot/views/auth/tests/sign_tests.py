from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
import jsonschema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from codepot.views.auth import auth_json_schema


class SignInTests(TestCase):
    client = APIClient()

    def test_if_sign_in_fails_when_no_body_sent(self):
        payload = None
        resp = self.client.post('/api/auth/sign-in/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['code'], 400)
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_in_fails_when_empty_body_sent(self):
        payload = {}
        resp = self.client.post('/api/auth/sign-in/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['code'], 400)
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_in_fails_when_no_password_sent(self):
        payload = {
            'email': 'lol@lol.com',
        }
        resp = self.client.post('/api/auth/sign-in/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("'password' is a required property" in resp.data['detail'])
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_in_fails_when_no_email_sent(self):
        payload = {
            'password': 'pass',
        }
        resp = self.client.post('/api/auth/sign-in/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("'email' is a required property" in resp.data['detail'])
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_in_fails_if_malformed_email_sent(self):
        payload = {
            'email': 'malformed',
            'password': 'pass',
        }
        resp = self.client.post('/api/auth/sign-in/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual('Incorrect username or password.', resp.data['detail'])
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_in_fails_if_bad_email_sent(self):
        payload = {
            'email': 'lol@lol.com',
            'password': 'pass',
        }
        resp = self.client.post('/api/auth/sign-in/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual('Incorrect username or password.', resp.data['detail'])
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_fails_if_invalid_password_sent(self):
        email = 'lol@lol.com'
        password = 'good'

        User.objects.create_user(email, email, make_password(password))

        payload = {
            'email': email,
            'password': 'bad',
        }
        resp = self.client.post('/api/auth/sign-in/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual('Incorrect username or password.', resp.data['detail'])
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_succeeds(self):
        email = 'lol@lol.com'
        password = 'good'
        first_name = 'lolf'
        last_name = 'loll'

        user = User.objects.create_user(email, email, password, first_name=first_name, last_name=last_name)
        token =Token.objects.create(user=user)

        payload = {
            'email': email,
            'password': password,
        }
        resp = self.client.post('/api/auth/sign-in/', payload, format='json')
        resp_data = resp.data
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp['Token'], token.key)

        jsonschema.validate(resp_data, auth_json_schema.auth_res_schema)

        self.assertEqual(resp_data['firstName'], first_name)
        self.assertEqual(resp_data['lastName'], last_name)
        self.assertEqual(resp_data['email'], email)
        self.assertEqual(resp_data['id'], user.id)


class SignUpTests(TestCase):
    client = APIClient()

    def test_if_sign_up_fails_when_no_body_sent(self):
        payload = None
        resp = self.client.post('/api/auth/sign-up/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['code'], 400)
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_up_fails_when_empty_body_sent(self):
        payload = {}
        resp = self.client.post('/api/auth/sign-up/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['code'], 400)
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_up_fails_when_no_password_sent(self):
        payload = {
            'email': 'lol@lol.com',
        }
        resp = self.client.post('/api/auth/sign-up/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("'password' is a required property" in resp.data['detail'])
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_up_fails_when_no_email_sent(self):
        payload = {
            'password': 'pass',
        }
        resp = self.client.post('/api/auth/sign-up/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("'email' is a required property" in resp.data['detail'])
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_up_fails_if_malformed_email_sent(self):
        payload = {
            'email': 'malformed',
            'firstName': 'lolf',
            'lastName': 'loll',
            'password': 'pass',
        }
        resp = self.client.post('/api/auth/sign-up/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Email address is not valid.', resp.data['detail'])
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_up_succeeds(self):
        email = 'lol@lol.com'
        password = 'good'
        first_name = 'lolf'
        last_name = 'loll'

        payload = {
            'email': email,
            'password': password,
            'firstName': first_name,
            'lastName': last_name,
        }
        resp = self.client.post('/api/auth/sign-up/', payload, format='json')
        resp_data = resp.data
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp['Token'], Token.objects.get().key)

        jsonschema.validate(resp_data, auth_json_schema.auth_res_schema)

        self.assertEqual(resp_data['firstName'], first_name)
        self.assertEqual(resp_data['lastName'], last_name)
        self.assertEqual(resp_data['email'], email)
        self.assertEqual(resp_data['id'], User.objects.get().id)

    def test_if_sign_up_fails_if_email_taken(self):
        email = 'lol@lol.com'
        password = 'good'
        first_name = 'lolf'
        last_name = 'loll'

        payload = {
            'email': email,
            'password': password,
            'firstName': first_name,
            'lastName': last_name,
        }
        resp = self.client.post('/api/auth/sign-up/', payload, format='json')
        resp_data = resp.data
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp['Token'], Token.objects.get().key)

        jsonschema.validate(resp_data, auth_json_schema.auth_res_schema)

        resp = self.client.post('/api/auth/sign-up/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
        self.assertFalse(resp.has_header('Token'))

        self.assertEqual('Email address already taken.', resp.data['detail'])

    def tearDown(self):
        User.objects.all().delete()
