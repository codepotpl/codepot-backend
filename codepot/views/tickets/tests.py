import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from codepot.models import (
    PriceTier,
    Product,
)


class PricesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='lol@lol.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

        self.price_early_name = 'NAME_1'
        self.price_early_1 = PriceTier.objects.create(
            name=self.price_early_name,
            date_from=timezone.now(),
            date_to=timezone.now() + datetime.timedelta(days=1),
        )
        self.price_early_name = 'NAME_2'
        self.price_early_2 = PriceTier.objects.create(
            name=self.price_early_name,
            date_from=timezone.now() + datetime.timedelta(days=2),
            date_to=timezone.now() + datetime.timedelta(days=4),
        )

        Product.objects.create(name='EARLY_1_FIRST_DAY', price_tier=self.price_early_1, price_net=5000,
                               price_total=6150)
        Product.objects.create(name='EARLY_1_SECOND_DAY', price_tier=self.price_early_1, price_net=5000,
                               price_total=6150)
        Product.objects.create(name='EARLY_1_BOTH_DAYS', price_tier=self.price_early_1, price_net=10000,
                               price_total=12300)

        Product.objects.create(name='EARLY_2_FIRST_DAY', price_tier=self.price_early_2, price_net=5000,
                               price_total=6150)
        Product.objects.create(name='EARLY_2_SECOND_DAY', price_tier=self.price_early_2, price_net=5000,
                               price_total=6150)
        Product.objects.create(name='EARLY_2_BOTH_DAYS', price_tier=self.price_early_2, price_net=10000,
                               price_total=12300)

    def test_correct_prices_response(self):
        resp = self.client.get('/api/tickets/prices/')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.data
        self.assertEqual(len(data['prices']), Product.objects.count())
        self.assertEqual(len(list(filter(lambda x: x['active'] == True, data['prices']))), 3)

    def tearDown(self):
        PriceTier.objects.all().delete()
        User.objects.all().delete()
        Token.objects.all().delete()
