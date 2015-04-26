from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
import jsonschema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from app.models import UserProfile
from app.views.auth import auth_json_schema


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
        self.assertEqual('Incorrect username or password', resp.data['detail'])
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_in_fails_if_bad_email_sent(self):
        payload = {
            'email': 'lol@lol.com',
            'password': 'pass',
        }
        resp = self.client.post('/api/auth/sign-in/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual('Incorrect username or password', resp.data['detail'])
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
        self.assertEqual('Incorrect username or password', resp.data['detail'])
        self.assertFalse(resp.has_header('Token'))

    def test_if_sign_succeeds(self):
        email = 'lol@lol.com'
        password = 'good'

        user = User.objects.create_user(email, email, password)
        UserProfile.objects.create(
            user=user,
            email=email,
            first_name='lolf',
            last_name='loll'
        )
        token =Token.objects.create(user=user)

        payload = {
            'email': email,
            'password': password,
        }
        resp = self.client.post('/api/auth/sign-in/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp['Token'], token.key)
        jsonschema.validate(resp.data, auth_json_schema.auth_res_schema)

