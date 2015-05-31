import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from djangopay.models import Product
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_201_CREATED)
from rest_framework.test import APIClient

from codepot.models import (
    Purchase,
    Ticket,
    TicketTypeName,
    Price,
)
from codepot.models.promo_codes import PromoCode


class NewPurchaseTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='lol@lol.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        self.req_format = 'json'

        self.price = Price.objects.create(
            name='EARLY',
            date_from=timezone.now(),
            date_to=timezone.now() + datetime.timedelta(days=1),
            first_day_net=5000,
            first_day_total=6150,
            second_day_net=5000,
            second_day_total=6150,
            both_days_net=10000,
            both_days_total=12300
        )

    def test_if_purchase_fails_when_no_authorization_token_sent(self):
        client = APIClient()
        payload = None
        resp = client.post('/api/purchases/new/', payload, format=self.req_format)
        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(resp.data['code'], 0)
        self.assertEqual(resp.data['detail'], 'Authentication credentials were not provided.')

        self.assertEqual(Purchase.objects.count(), 0)


    def test_if_purchase_fails_when_invalid_body_sent(self):
        payload = {}
        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['code'], 400)

        self.assertEqual(Purchase.objects.count(), 0)

    def test_if_exception_raised_when_user_has_purchase(self):
        ticket = Ticket.objects.create(type=TicketTypeName.FIRST_DAY.value)
        purchase = Purchase.objects.create(user=self.user, ticket=ticket, price=self.price)

        payload = {
            'promoCode': None,
            'invoice': None,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_409_CONFLICT)
        self.assertEqual(resp.data['code'], 304)
        self.assertEqual(resp.data['detail'], 'User: {} already has purchase: {}.'.format(self.user.id, purchase.id))

        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

    def test_if_purchase_is_created_and_returned_without_promo_code_and_without_invoice(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.assertEqual(Purchase.objects.count(), 0)
        self.assertEqual(Ticket.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

        purchase = Purchase.objects.get()
        ticket = Ticket.objects.get()

        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        self.assertEqual(resp.data['purchaseId'], purchase.id)

        self.assertEqual(purchase.ticket, ticket)
        self.assertEqual(purchase.price, self.price)
        self.assertIsNone(purchase.invoice_name)
        self.assertIsNone(purchase.invoice_street)
        self.assertIsNone(purchase.invoice_tax_id)
        self.assertIsNone(purchase.invoice_zip_code)
        self.assertIsNone(purchase.invoice_country)
        self.assertIsNone(purchase.promo_code)

        self.assertEqual(ticket.type, TicketTypeName.FIRST_DAY.value)

    def test_if_purchase_is_created_and_returned_without_promo_code_and_with_invoice(self):
        invoice = {
            'name': 'Name',
            'street': 'Street',
            'zipCode': '00-000',
            'country': 'Country',
            'taxId': '0123456789',
        }
        payload = {
            'promoCode': None,
            'invoice': invoice,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.assertEqual(Purchase.objects.count(), 0)
        self.assertEqual(Ticket.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

        purchase = Purchase.objects.get()
        ticket = Ticket.objects.get()

        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        self.assertEqual(resp.data['purchaseId'], purchase.id)

        self.assertEqual(purchase.ticket, ticket)
        self.assertEqual(purchase.price, self.price)
        self.assertEqual(purchase.invoice_name, invoice['name'])
        self.assertEqual(purchase.invoice_street, invoice['street'])
        self.assertEqual(purchase.invoice_tax_id, invoice['taxId'])
        self.assertEqual(purchase.invoice_zip_code, invoice['zipCode'])
        self.assertEqual(purchase.invoice_country, invoice['country'])
        self.assertIsNone(purchase.promo_code)

        self.assertEqual(ticket.type, TicketTypeName.FIRST_DAY.value)

    def test_response_when_non_existing_promo_code_used(self):
        payload = {
            'promoCode': '123456',
            'invoice': None,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)
        self.assertEqual(resp.status_code, HTTP_409_CONFLICT)
        self.assertEqual(resp.data['code'], 301)
        self.assertEqual(resp.data['detail'], 'Given promo code: 123456, does not exist.')

        self.assertEqual(Purchase.objects.count(), 0)

    def test_response_when_inactive_promo_code_used(self):
        promo_code = PromoCode.objects.create(active=False)

        payload = {
            'promoCode': promo_code.code,
            'invoice': None,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)
        self.assertEqual(resp.status_code, HTTP_409_CONFLICT)
        self.assertEqual(resp.data['code'], 302)
        self.assertEqual(resp.data['detail'], 'Given promo code: {} is not active.'.format(promo_code.code))

        self.assertEqual(Purchase.objects.count(), 0)

    def tearDown(self):
        Price.objects.all().delete()
        Product.objects.all().delete()
        Purchase.objects.all().delete()
        Ticket.objects.all().delete()
        User.objects.all().delete()
