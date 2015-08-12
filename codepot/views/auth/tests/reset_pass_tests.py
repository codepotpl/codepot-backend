import random

from django.contrib.auth.hashers import (
  make_password,
  check_password,
)
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.test import APIClient
from django.test import TestCase

from codepot.models import ResetPassword


class ResetPasswordTest(TestCase):
  client = APIClient()

  def test_if_sign_in_fails_when_no_body_sent(self):
    payload = None
    resp = self.client.post('/api/auth/reset-pass/initialize/', payload, format='json')
    self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(resp.data['code'], 400)
    self.assertFalse(resp.has_header('Token'))

  def test_if_exception_raised_if_email_not_found(self):
    payload = {'email': 'lol@lol.com'}
    resp = self.client.post('/api/auth/reset-pass/initialize/', payload, format='json')
    self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
    self.assertIsNone(resp.data)

  def test_if_previous_reset_pw_attempts_are_removed(self):
    email = 'lol@lol.com'
    User.objects.create_user(str(random.random()), email=email)

    self.assertEqual(ResetPassword.objects.count(), 0)

    payload = {
      'email': email,
    }

    self.client.post('/api/auth/reset-pass/initialize/', payload, format='json')
    self.assertEqual(ResetPassword.objects.count(), 1)
    self.assertEqual(ResetPassword.objects.filter(email=email).count(), 1)

    self.client.post('/api/auth/reset-pass/initialize/', payload, format='json')
    self.assertEqual(ResetPassword.objects.filter(email=email).count(), 1)
    self.assertEqual(ResetPassword.objects.count(), 1)

  def test_if_exception_raised_if_no_reset_password_record_found(self):
    payload = {
      'token': '-1',
      'password': 'password',
    }
    resp = self.client.post('/api/auth/reset-pass/finalize/', payload, format='json')
    self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

    self.assertEqual(resp.data['code'], 107)
    self.assertEqual(resp.data['detail'], 'No entry found for token sent.')

  def test_if_exception_raised_if_reset_password_found_but_user_not_found(self):
    email = 'lol@lol.com'
    token = '-1'
    ResetPassword.objects.create(email=email, token=token, active=True)

    payload = {
      'token': token,
      'password': 'password',
    }
    resp = self.client.post('/api/auth/reset-pass/finalize/', payload, format='json')
    self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

    self.assertEqual(resp.data['code'], 106)
    self.assertEqual(resp.data['detail'], 'User not found for given email.')

  def test_if_the_whole_reset_password_flow_works(self):
    email = 'lol@lol.com'
    old_password = 'old'
    new_password = 'password'
    user = User.objects.create_user(str(random.random()), email=email, password=old_password)

    self.assertTrue(check_password(old_password, user.password))

    payload = {
      'email': email,
    }

    self.client.post('/api/auth/reset-pass/initialize/', payload, format='json')
    self.assertEqual(ResetPassword.objects.count(), 1)
    self.assertTrue(check_password(old_password, user.password))

    token = ResetPassword.objects.get(email=email).token
    self.assertEqual(ResetPassword.objects.filter(email=email, token=token, active=True).count(), 1)

    payload = {
      'token': token,
      'password': new_password,
    }

    resp = self.client.post('/api/auth/reset-pass/finalize/', payload, format='json')
    self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)
    self.assertIsNone(resp.data)

    self.assertEqual(ResetPassword.objects.count(), 1)
    self.assertEqual(ResetPassword.objects.filter(email=email, token=token, active=False).count(), 1)

    user = User.objects.get(email=email)

    self.assertFalse(check_password(old_password, user.password))
    self.assertTrue(check_password(new_password, user.password))

  def tearDown(self):
    ResetPassword.objects.all().delete()
    User.objects.all().delete()
