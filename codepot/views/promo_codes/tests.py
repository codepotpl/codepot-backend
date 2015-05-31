from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.test import APIClient

from codepot.models import PromoCode


class PromoCodeTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='lol@lol.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

    def test_response_for_existing_promo_code(self):
        promo_code = PromoCode.objects.create()
        resp = self.client.get('/api/promo-codes/{}/'.format(promo_code.code))
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertEqual(resp.data['code'], promo_code.code)
        self.assertEqual(resp.data['active'], promo_code.active)
        self.assertEqual(resp.data['discount'], promo_code.discount)

    def test_response_for_non_existing_promo_code(self):
        resp = self.client.get('/api/promo-codes/lol/')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(resp.data['code'], 200)
        self.assertEqual(resp.data['detail'], 'Promo code for ID: lol, not found.')

    def tearDown(self):
        PromoCode.objects.all().delete()
