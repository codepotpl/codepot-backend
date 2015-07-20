import datetime
import random

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_201_CREATED,
    HTTP_410_GONE,
)
from rest_framework.test import APIClient

from codepot.models import (
    Purchase,
    PurchaseInvoice,
    Ticket,
    PriceTier,
    PromoCode,
    PromoCodeClassification,
    PaymentTypeName,
    Product,
    PaymentStatusName,
    AppSettings,
    AppSettingName,
)


class NewPurchaseTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='lol@lol.com')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        self.req_format = 'json'

        self.price_name = 'EARLY'
        self.price_tier = PriceTier.objects.create(
            name=self.price_name,
            date_from=timezone.now(),
            date_to=timezone.now() + datetime.timedelta(days=1)
        )
        self.product = Product.objects.create(name='EARLY_FIRST_DAY', price_tier=self.price_tier, price_net=5000)

    def test_if_purchase_fails_when_no_authorization_token_sent(self):
        client = APIClient()

        resp = client.post('/api/purchases/new/', None, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(resp.data['code'], 0)
        self.assertEqual(resp.data['detail'], 'Authentication credentials were not provided.')

        self.assertEqual(Purchase.objects.count(), 0)

    def test_if_purchase_fails_when_invalid_body_sent(self):
        resp = self.client.post('/api/purchases/new/', {}, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['code'], 400)

        self.assertEqual(Purchase.objects.count(), 0)

    def test_if_exception_raised_when_user_has_purchase(self):
        purchase = Purchase.objects.create(user=self.user, product=self.product)

        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_409_CONFLICT)
        self.assertEqual(resp.data['code'], 304)
        self.assertEqual(resp.data['detail'], 'User: {} already has purchase: {}.'.format(self.user.id, purchase.id))

    def test_if_exception_raised_when_invalid_product_id_sent(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': str(int(random.random())),
            'paymentType': PaymentTypeName.TRANSFER.value,
            'paymentInfo': None,
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_409_CONFLICT)
        self.assertEqual(resp.data['code'], 305)
        self.assertEqual(resp.data['detail'], 'Product for ID: {}, not found.'.format(payload['productId']))

    def test_if_exception_raised_when_product_is_inactive(self):
        price_tier = PriceTier.objects.create(
            name='RANDOM_PRICE_TIER',
            date_from=timezone.now() - datetime.timedelta(days=2),
            date_to=timezone.now() - datetime.timedelta(days=1)
        )
        product = Product.objects.create(name='RANDOM_FIRST_DAY', price_tier=price_tier, price_net=5000)

        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': product.id,
            'paymentType': PaymentTypeName.TRANSFER.value,
            'paymentInfo': None,
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_409_CONFLICT)
        self.assertEqual(resp.data['code'], 306)
        self.assertEqual(resp.data['detail'], 'Product for ID: {} is not active.'.format(product.id))

    def test_if_exception_raised_when_registration_closed(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': 'random',
            'paymentType': PaymentTypeName.TRANSFER.value,
            'paymentInfo': None,
        }
        open = AppSettings.objects.get(name=AppSettingName.CDPT_REGISTRATION_OPEN.value)
        open.value = False
        open.save()

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_410_GONE)
        self.assertEqual(resp.data['code'], 400)
        self.assertEqual(resp.data['detail'], 'Registration closed')

    def test_if_no_new_objects_created_when_exception_occurs(self):
        Purchase.objects.create(user=self.user, product=self.product)

        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
        }

        self.assertEqual(Purchase.objects.count(), 1)

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)

    def test_if_new_purchase_objects_created_and_relations_established_on_successful_flow(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        self.assertEqual(Purchase.objects.count(), 0)
        self.assertEqual(Ticket.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        self.assertEqual(Purchase.objects.count(), 1)

        purchase = Purchase.objects.get()


        self.assertEqual(resp.data['purchase']['id'], purchase.id)
        self.assertEqual(purchase.payment_type, PaymentTypeName.PAYU.value)
        self.assertEqual(purchase.user, self.user)
        self.assertEqual(purchase.payment_status, PaymentStatusName.PENDING.value)
        self.assertIsNone(purchase.promo_code)
        self.assertIsNotNone(purchase.payu_payment)

    def test_if_invoice_data_ignored_when_not_sent(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        self.assertEqual(PurchaseInvoice.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        self.assertEqual(PurchaseInvoice.objects.count(), 0)

    def test_if_invoice_data_saved_when_sent(self):
        invoice = {
            'name': 'Name',
            'street': 'Street',
            'zipCode': '00-000',
            'city': 'City',
            'country': 'Country',
            'taxId': '0123456789',
        }
        payload = {
            'promoCode': None,
            'invoice': invoice,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        purchase = Purchase.objects.get()
        purchase_invoice = PurchaseInvoice.objects.get(purchase=purchase)
        self.assertEqual(purchase_invoice.name, invoice['name'])
        self.assertEqual(purchase_invoice.street, invoice['street'])
        self.assertEqual(purchase_invoice.tax_id, invoice['taxId'])
        self.assertEqual(purchase_invoice.zip_code, invoice['zipCode'])
        self.assertEqual(purchase_invoice.city, invoice['city'])
        self.assertEqual(purchase_invoice.country, invoice['country'])
        self.assertEqual(purchase.payment_type, PaymentTypeName.PAYU.value)
        self.assertEqual(purchase.payment_status, PaymentStatusName.PENDING.value)

    def test_if_tickets_purchased_field_is_increased_when_purchase_succeeds(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        self.assertEqual(self.price_tier.tickets_purchased, 0)

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        price = PriceTier.objects.get(name=self.price_name)
        self.assertEqual(price.tickets_purchased, 1)

    def test_response_when_non_existing_promo_code_used(self):
        payload = {
            'promoCode': '1234567890',
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)
        self.assertEqual(resp.status_code, HTTP_409_CONFLICT)
        self.assertEqual(resp.data['code'], 301)
        self.assertEqual(resp.data['detail'], 'Given promo code: 1234567890, does not exist.')

        self.assertEqual(Purchase.objects.count(), 0)

    def test_response_when_inactive_promo_code_used(self):
        promo_code = PromoCode.objects.create(active=False)

        payload = {
            'promoCode': promo_code.code,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
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
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
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
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        promo_code = PromoCode.objects.get()
        self.assertEqual(promo_code.usage_limit, 0)

    def test_if_no_payment_created_for_100_percent_discount_code(self):
        promo_code = PromoCode.objects.create(discount=100)

        payload = {
            'promoCode': promo_code.code,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()
        self.assertIsNone(purchase.payu_payment)

    def test_if_FREE_purchase_type_set_for_100_percent_discount_promo_code(self):
        promo_code = PromoCode.objects.create(discount=100)

        payload = {
            'promoCode': promo_code.code,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()
        self.assertEqual(purchase.payment_type, PaymentTypeName.FREE.value)
        self.assertEqual(purchase.payment_status, PaymentStatusName.SUCCESS.value)

    def test_if_GROUP_purchase_type_set_for_100_percent_discount_promo_code(self):
        promo_code_classification = PromoCodeClassification.objects.create(name='group-lol')
        promo_code = PromoCode.objects.create(discount=100, classification=promo_code_classification)

        payload = {
            'promoCode': promo_code.code,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()
        self.assertEqual(purchase.payment_type, PaymentTypeName.GROUP.value)
        self.assertEqual(purchase.payment_status, PaymentStatusName.SUCCESS.value)


    def test_in_invoice_is_skipped_for_100_percent_promo_code(self):
        promo_code = PromoCode.objects.create(discount=100)
        invoice = {
            'name': 'Name',
            'street': 'Street',
            'zipCode': '00-000',
            'city': 'City',
            'country': 'Country',
            'taxId': '0123456789',
        }

        payload = {
            'promoCode': promo_code.code,
            'invoice': invoice,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        self.assertEqual(PurchaseInvoice.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_201_CREATED)

        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(PurchaseInvoice.objects.count(), 0)

    def test_if_price_is_reduced_with_discount(self):
        discount = 10
        promo_code = PromoCode.objects.create(discount=discount)
        invoice = {
            'name': 'Name',
            'street': 'Street',
            'zipCode': '00-000',
            'city': 'City',
            'country': 'Country',
            'taxId': '0123456789',
        }

        payload = {
            'promoCode': promo_code.code,
            'invoice': invoice,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()
        payu_payment = purchase.payu_payment
        self.assertIsNotNone(payu_payment)
        expected_price = (self.product.price_net - (discount * self.product.price_net / 100)) * (
            1.0 + self.product.price_vat)
        self.assertEqual(payu_payment.total_price, expected_price)

    def test_note_is_saved_when_transfer_purchase_chosen(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.TRANSFER.value,
            'paymentInfo': None,
        }

        self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()
        self.assertIsNone(purchase.payu_payment)
        self.assertEqual(purchase.payment_type, PaymentTypeName.TRANSFER.value)
        self.assertEqual(purchase.notes, 'To pay net: {}, total: {}'.format(self.product.price_net,
                                                                            int(self.product.price_net * (
                                                                                1 + self.product.price_vat))))

    def test_successful_response_for_transfer(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.TRANSFER.value,
            'paymentInfo': None,
        }
        self.assertEqual(Purchase.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()

        payment_info = resp.data['purchase']['paymentInfo']
        transfer_data = payment_info['transferData']
        self.assertEqual(transfer_data['accountNo'], '81109028510000000122488798')
        self.assertEqual(transfer_data['street'], 'Osowska 23/6')
        self.assertEqual(transfer_data['zipCode'], '04-302')
        self.assertEqual(transfer_data['city'], 'Warszawa')
        self.assertEqual(transfer_data['title'], 'Codepot: {}'.format(purchase.id))

        self.assertEqual(purchase.payment_status, PaymentStatusName.PENDING.value)

    def test_successful_response_for_payu(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }
        self.assertEqual(Purchase.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)

        payment_info = resp.data['purchase']['paymentInfo']
        payment_link = payment_info['paymentLink']
        self.assertIsNotNone(payment_link)

        self.assertEqual(Purchase.objects.get().payment_status, PaymentStatusName.PENDING.value)

    def test_whole_successful_response_for_transfer(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.TRANSFER.value,
            'paymentInfo': None,
        }
        self.assertEqual(Purchase.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)
        purchase = Purchase.objects.get()

        resp_data = resp.data
        payment_info = resp_data['purchase']['paymentInfo']
        transfer_data = payment_info['transferData']
        self.assertEqual(transfer_data['accountNo'], '81109028510000000122488798')
        self.assertEqual(transfer_data['street'], 'Osowska 23/6')
        self.assertEqual(transfer_data['zipCode'], '04-302')
        self.assertEqual(transfer_data['city'], 'Warszawa')
        self.assertEqual(transfer_data['title'], 'Codepot: {}'.format(purchase.id))
        self.assertEqual(resp_data['purchase']['id'], purchase.id)
        self.assertEqual(resp_data['purchase']['paymentType'], purchase.payment_type)
        self.assertEqual(resp_data['purchase']['priceNet'], purchase.price_net)
        self.assertEqual(resp_data['purchase']['priceTotal'], purchase.price_total)
        self.assertEqual(resp_data['purchase']['priceTotal'], self.product.price_net * (1 + self.product.price_vat))

        self.assertEqual(purchase.payment_status, PaymentStatusName.PENDING.value)

    def test_whole_successful_response_for_payu(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': {'redirectLink': 'link', },
        }
        self.assertEqual(Purchase.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(Purchase.objects.count(), 1)

        purchase = Purchase.objects.get()

        resp_data = resp.data
        payment_info = resp_data['purchase']['paymentInfo']
        payment_link = payment_info['paymentLink']
        self.assertIsNotNone(payment_link)
        self.assertEqual(resp_data['purchase']['id'], purchase.id)
        self.assertEqual(resp_data['purchase']['paymentType'], purchase.payment_type)
        self.assertEqual(resp_data['purchase']['priceNet'], purchase.price_net)
        self.assertEqual(resp_data['purchase']['priceTotal'], self.product.price_net * (1 + self.product.price_vat))

        self.assertEqual(Purchase.objects.get().payment_status, PaymentStatusName.PENDING.value)

    def test_if_exception_thrown_when_no_redirect_link_sent_with_payu_payment(self):
        payload = {
            'promoCode': None,
            'invoice': None,
            'productId': self.product.id,
            'paymentType': PaymentTypeName.PAYU.value,
            'paymentInfo': None,
        }
        self.assertEqual(Purchase.objects.count(), 0)

        resp = self.client.post('/api/purchases/new/', payload, format=self.req_format)

        self.assertEqual(resp.status_code, HTTP_409_CONFLICT)
        self.assertEqual(resp.data['code'], 307)
        self.assertEqual(resp.data['detail'], "'redirectLink' is required for PAYU payment type.")

    def tearDown(self):
        PriceTier.objects.all().delete()
        Product.objects.all().delete()
        Purchase.objects.all().delete()
        Ticket.objects.all().delete()
        User.objects.all().delete()
        PromoCode.objects.all().delete()
        PromoCodeClassification.objects.all().delete()
