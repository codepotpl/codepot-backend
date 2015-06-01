import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
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
    PriceTier,
    PromoCode,
    PurchaseTypeName,
    Product)


class NewPurchaseTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='lol@lol.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        self.req_format = 'json'

        self.price_name = 'EARLY'
        self.price = PriceTier.objects.create(
            name=self.price_name,
            date_from=timezone.now(),
            date_to=timezone.now() + datetime.timedelta(days=1)
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
        purchase = Purchase.objects.create(user=self.user, ticket=ticket)  # TODO price

        payload = {
            'promoCode': None,
            'invoice': None,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_409_CONFLICT)
        self.assertEqual(resp.data['code'], 304)
        self.assertEqual(resp.data['detail'], 'User: {} already has purchase: {}.'.format(self.user.id, purchase.id))

    def test_if_no_new_objects_created_when_exception_occurs(self):
        ticket = Ticket.objects.create(type=TicketTypeName.FIRST_DAY.value)
        Purchase.objects.create(user=self.user, ticket=ticket)  # TODO , price=self.price)

        payload = {
            'promoCode': None,
            'invoice': None,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

    def test_if_new_purchase_objects_created_and_relations_established_on_successful_flow(self):
        payload = {
            'promoCode': None,
            'purchaseType': PurchaseTypeName.PAYU.value,
            'invoice': None,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.assertEqual(Purchase.objects.count(), 0)
        self.assertEqual(Ticket.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

        purchase = Purchase.objects.get()
        ticket = Ticket.objects.get()

        self.assertEqual(resp.data['purchaseId'], purchase.id)
        self.assertEqual(purchase.ticket, ticket)
        self.assertEqual(purchase.type, PurchaseTypeName.PAYU.value)
        # self.assertEqual(purchase.price, self.price) #TODO
        self.assertEqual(purchase.user, self.user)
        self.assertIsNone(purchase.promo_code)
        # TODO payment

        self.assertEqual(ticket.type, TicketTypeName.FIRST_DAY.value)

    def test_if_invoice_data_ignored_when_not_sent(self):
        payload = {
            'promoCode': None,
            'purchaseType': PurchaseTypeName.PAYU.value,
            'invoice': None,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        purchase = Purchase.objects.get()

        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        self.assertEqual(resp.data['purchaseId'], purchase.id)

        self.assertIsNone(purchase.invoice_name)
        self.assertIsNone(purchase.invoice_street)
        self.assertIsNone(purchase.invoice_tax_id)
        self.assertIsNone(purchase.invoice_zip_code)
        self.assertIsNone(purchase.invoice_country)

    def test_if_invoice_data_saved_when_sent(self):
        invoice = {
            'name': 'Name',
            'street': 'Street',
            'zipCode': '00-000',
            'country': 'Country',
            'taxId': '0123456789',
        }
        payload = {
            'promoCode': None,
            'purchaseType': PurchaseTypeName.PAYU.value,
            'invoice': invoice,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        purchase = Purchase.objects.get()
        self.assertEqual(purchase.invoice_name, invoice['name'])
        self.assertEqual(purchase.invoice_street, invoice['street'])
        self.assertEqual(purchase.invoice_tax_id, invoice['taxId'])
        self.assertEqual(purchase.invoice_zip_code, invoice['zipCode'])
        self.assertEqual(purchase.invoice_country, invoice['country'])
        self.assertEqual(purchase.type, PurchaseTypeName.PAYU.value)

    def test_if_tickets_purchased_field_is_increased_when_purchase_succeeds(self):
        payload = {
            'promoCode': None,
            'purchaseType': PurchaseTypeName.PAYU.value,
            'invoice': None,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.assertEqual(self.price.tickets_purchased, 0)

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        price = PriceTier.objects.get(name=self.price_name)
        self.assertEqual(price.tickets_purchased, 1)

    def test_response_when_non_existing_promo_code_used(self):
        payload = {
            'promoCode': '123456',
            'invoice': None,
            'purchaseType': PurchaseTypeName.PAYU.value,
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
            'purchaseType': PurchaseTypeName.PAYU.value,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)
        self.assertEqual(resp.status_code, HTTP_409_CONFLICT)
        self.assertEqual(resp.data['code'], 302)
        self.assertEqual(resp.data['detail'], 'Given promo code: {} is not active.'.format(promo_code.code))

        self.assertEqual(Purchase.objects.count(), 0)

    def test_if_promo_code_is_assigned_to_purchase(self):
        promo_code = PromoCode.objects.create()

        payload = {
            'promoCode': promo_code.code,
            'invoice': None,
            'purchaseType': PurchaseTypeName.PAYU.value,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()
        self.assertEqual(purchase.promo_code, promo_code)

    def test_if_promo_code_usage_limit_decremented(self):
        promo_code = PromoCode.objects.create()
        self.assertEqual(promo_code.usage_limit, 1)

        payload = {
            'promoCode': promo_code.code,
            'invoice': None,
            'purchaseType': PurchaseTypeName.PAYU.value,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        promo_code = PromoCode.objects.get()
        self.assertEqual(promo_code.usage_limit, 0)

    def test_if_no_payment_created_for_100_percent_discount_code(self):
        promo_code = PromoCode.objects.create(discount=100)

        payload = {
            'promoCode': promo_code.code,
            'invoice': None,
            'purchaseType': PurchaseTypeName.PAYU.value,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()
        self.assertIsNone(purchase.payment)

    def test_if_FREE_purchase_type_set_for_100_percent_discount_promo_code(self):
        promo_code = PromoCode.objects.create(discount=100)

        payload = {
            'promoCode': promo_code.code,
            'invoice': None,
            'purchaseType': PurchaseTypeName.PAYU.value,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()
        self.assertEqual(purchase.type, PurchaseTypeName.FREE.value)

    def test_in_invoice_is_skipped_for_100_percent_promo_code(self):
        promo_code = PromoCode.objects.create(discount=100)
        invoice = {
            'name': 'Name',
            'street': 'Street',
            'zipCode': '00-000',
            'country': 'Country',
            'taxId': '0123456789',
        }

        payload = {
            'promoCode': promo_code.code,
            'invoice': invoice,
            'purchaseType': PurchaseTypeName.PAYU.value,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()
        self.assertIsNone(purchase.invoice_name)
        self.assertIsNone(purchase.invoice_street)
        self.assertIsNone(purchase.invoice_tax_id)
        self.assertIsNone(purchase.invoice_zip_code)
        self.assertIsNone(purchase.invoice_country)

    # TODO
    def test_if_price_is_reduced_with_discount(self):
        promo_code = PromoCode.objects.create(discount=10)
        invoice = {
            'name': 'Name',
            'street': 'Street',
            'zipCode': '00-000',
            'country': 'Country',
            'taxId': '0123456789',
        }

        payload = {
            'promoCode': promo_code.code,
            'invoice': invoice,
            'purchaseType': PurchaseTypeName.PAYU.value,
            'ticketType': TicketTypeName.FIRST_DAY.value,
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)

    # TODO
    def test_successful_response(self):
        pass

    def tearDown(self):
        PriceTier.objects.all().delete()
        Product.objects.all().delete()
        Purchase.objects.all().delete()
        Ticket.objects.all().delete()
        User.objects.all().delete()
        PromoCode.objects.all().delete()
