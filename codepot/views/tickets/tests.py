import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from codepot.models import Price


class PricesTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='lol@lol.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))

        self.price_early_name = 'NAME_1'
        self.price_early = Price.objects.create(
            name=self.price_early_name,
            date_from=timezone.now(),
            date_to=timezone.now() + datetime.timedelta(days=1),
            first_day_net=5000,
            first_day_total=6150,
            second_day_net=5000,
            second_day_total=6150,
            both_days_net=10000,
            both_days_total=12300
        )
        self.price_early_name = 'NAME_2'
        self.price_early = Price.objects.create(
            name=self.price_early_name,
            date_from=timezone.now() + datetime.timedelta(days=2),
            date_to=timezone.now() + datetime.timedelta(days=4),
            first_day_net=50000,
            first_day_total=61500,
            second_day_net=50000,
            second_day_total=61500,
            both_days_net=100000,
            both_days_total=123000
        )

    def test_if_purchase_fails_when_invalid_body_sent(self):
        resp = self.client.get('/api/tickets/prices/')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = resp.data
        self.assertEqual(len(data['prices']), Price.objects.count())
        self.assertEqual(len(list(filter(lambda x: x['active'] == True, data['prices']))), 1)

    def tearDown(self):
        Price.objects.all().delete()
        User.objects.all().delete()
        Token.objects.all().delete()
