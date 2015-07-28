import datetime
from random import randint

from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.status import (
  HTTP_400_BAD_REQUEST,
  HTTP_403_FORBIDDEN,
  HTTP_404_NOT_FOUND,
  HTTP_409_CONFLICT,
  HTTP_204_NO_CONTENT)
from rest_framework.test import APIClient

from codepot.models import (
  Workshop,
  PriceTier,
  Product,
  Purchase,
  PaymentStatusName,
  TimeSlotTier,
  TimeSlotTierDayName,
  TimeSlot,
)


class UserWorkshopsTest(TestCase):
  def setUp(self):
    self.req_format = 'json'
    self.client = APIClient()

    self.attendee = User.objects.create(username='a', first_name='FA', last_name='LA')
    self.attendee_token = Token.objects.create(user=self.attendee)

    self.price_tier = PriceTier.objects.create(
      name='EARLY',
      date_from=timezone.now(),
      date_to=timezone.now() + datetime.timedelta(days=1)
    )
    self.product = Product.objects.create(name='EARLY_FIRST_DAY', price_tier=self.price_tier, price_net=5000)
    Purchase.objects.create(product=self.product, user=self.attendee, payment_status=PaymentStatusName.SUCCESS.value)

    self.workshop = Workshop.objects.create(
      title='Workshop',
      description='Description with a few words'
    )

    self.timeslot_tier = TimeSlotTier.objects.create(date_from=datetime.datetime.now(), date_to=datetime.datetime.now(),
                                                     day=TimeSlotTierDayName.FIRST.value)

    TimeSlot.objects.create(room_no=102, timeslot_tier=self.timeslot_tier, workshop=self.workshop)

    self.req_format = 'json'
    self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.attendee_token.key))

  def test_if_exception_raised_when_user_id_and_token_does_not_match_when_getting_list_of_workshops(self):
    resp = self.client.get('/api/users/{}/workshops/'.format(randint(3000, 4000)), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)

    data = resp.data
    self.assertEqual(data['code'], 105)
    self.assertEqual(data['detail'], 'Invalid user ID exception.')

  def test_if_validation_fails_when_invalid_body_sent_with_sign_request(self):
    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), {}, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    data = resp.data
    self.assertEqual(data['code'], 0)
    self.assertEqual(data['detail'], "'workshopId' is a required property")

  def test_if_exception_raised_when_user_id_and_token_does_not_match_when_signing_for_workshop(self):
    resp = self.client.get('/api/users/{}/workshops/'.format(randint(3000, 4000)), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)

    data = resp.data
    self.assertEqual(data['code'], 105)
    self.assertEqual(data['detail'], 'Invalid user ID exception.')

  def test_if_exception_raised_if_user_signs_for_workshop_without_any_purchase(self):
    attendee = User.objects.create(username='b', first_name='FB', last_name='LB')
    attendee_token = Token.objects.create(user=attendee)

    self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(attendee_token.key))

    payload = {
      'workshopId': '0123456789'
    }

    resp = self.client.post('/api/users/{}/workshops/'.format(attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 504)
    self.assertEqual(data['detail'], 'User with ID: {} does not have valid purchase.'.format(attendee.id))

  def test_if_exception_raised_if_user_signs_for_workshop_without_successful_purchase(self):
    attendee = User.objects.create(username='b', first_name='FB', last_name='LB')
    attendee_token = Token.objects.create(user=attendee)

    Purchase.objects.create(product=self.product, user=attendee)

    self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(attendee_token.key))

    payload = {
      'workshopId': '0123456789'
    }

    resp = self.client.post('/api/users/{}/workshops/'.format(attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 504)
    self.assertEqual(data['detail'], 'User with ID: {} does not have valid purchase.'.format(attendee.id))

  def test_if_exception_raised_if_user_signs_for_workshop_that_does_not_exist(self):
    payload = {
      'workshopId': '0123456789'
    }
    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    data = resp.data
    self.assertEqual(data['code'], 501)
    self.assertEqual(data['detail'], 'Workshop with ID: {} not found'.format(payload['workshopId']))

  def test_if_exception_raised_if_user_already_signed_for_workshop(self):
    self.workshop.attendees.add(self.attendee)

    payload = {
      'workshopId': self.workshop.id
    }
    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 505)
    self.assertEqual(data['detail'],
                     'User with ID: {} already signed for workshop with ID: {}.'.format(self.attendee.id,
                                                                                        self.workshop.id)
                     )

  def test_if_exception_raised_if_mentor_signs_for_own_workshop(self):
    mentor = User.objects.create(username='m', first_name='FM', last_name='LM')
    mentor_token = Token.objects.create(user=mentor)
    self.workshop.mentors.add(mentor)

    Purchase.objects.create(product=self.product, user=mentor, payment_status=PaymentStatusName.SUCCESS.value)

    self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(mentor_token.key))

    payload = {
      'workshopId': self.workshop.id
    }
    resp = self.client.post('/api/users/{}/workshops/'.format(mentor.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 506)
    self.assertEqual(data['detail'],
                     'User with ID: {} is workshop with ID: {} mentor.'.format(mentor.id,
                                                                               self.workshop.id)
                     )

  def test_if_exception_raised_when_workshop_limit_exceeded(self):
    workshop = self.workshop = Workshop.objects.create(title='t', description='d', max_attendees=0)

    payload = {
      'workshopId': workshop.id
    }

    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 507)
    self.assertEqual(data['detail'],
                     'Max attendees limit ({}) reached for workshop with ID: {}.'.format(workshop.max_attendees,
                                                                                         workshop.id))

  def test_if_exception_thrown_if_user_already_signed_for_workshop_in_the_same_slot(self):
    other_workshop = Workshop.objects.create(title='t', description='d', max_attendees=5)
    other_workshop.attendees.add(self.attendee)

    TimeSlot.objects.create(room_no=103, timeslot_tier=self.timeslot_tier, workshop=other_workshop)

    payload = {
      'workshopId': self.workshop.id
    }

    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 508)
    self.assertTrue(data['detail'].startswith(
      'User with ID: {}, is already registered for workshop in tier(s):'.format(self.attendee.id)))

  def test_if_user_successfully_registers_for_workshop(self):
    self.assertEqual(self.workshop.attendees.count(), 0)

    payload = {
      'workshopId': self.workshop.id
    }

    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)

    self.assertIsNone(resp.data)

    self.assertEqual(self.workshop.attendees.count(), 1)
    self.assertIn(self.attendee, self.workshop.attendees.all())

  def test_if_user_successfully_registers_for_workshop_and_then_fails_for_the_same_workshop(self):
    self.assertEqual(self.workshop.attendees.count(), 0)

    payload = {
      'workshopId': self.workshop.id
    }

    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)

    self.assertIsNone(resp.data)

    self.assertEqual(self.workshop.attendees.count(), 1)
    self.assertIn(self.attendee, self.workshop.attendees.all())

    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 505)
    self.assertEqual(data['detail'],
                     'User with ID: {} already signed for workshop with ID: {}.'.format(self.attendee.id,
                                                                                        self.workshop.id)
                     )

    self.assertEqual(self.workshop.attendees.count(), 1)
    self.assertIn(self.attendee, self.workshop.attendees.all())

  def tearDown(self):
    self.client.credentials(HTTP_AUTHORIZATION=None)
    Workshop.objects.all().delete()
    User.objects.all().delete()
    Purchase.objects.all().delete()
    Product.objects.all().delete()
    PriceTier.objects.all().delete()
