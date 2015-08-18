import datetime
from random import randint

import jsonschema
from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.status import (
  HTTP_400_BAD_REQUEST,
  HTTP_403_FORBIDDEN,
  HTTP_404_NOT_FOUND,
  HTTP_409_CONFLICT,
  HTTP_204_NO_CONTENT,
  HTTP_200_OK,
  HTTP_410_GONE,
)
from rest_framework.test import APIClient

from codepot.models import (
  Workshop,
  PriceTier,
  Product,
  Purchase,
  PaymentStatusName,
  TimeSlotTier,
  TimeSlot,
  TimeSlotTierDayName,
  WorkshopTag,
  AppSettings,
  AppSettingName,
)
from codepot.views.workshops import workshops_json_schema


class UserWorkshopsTest(TestCase):
  def setUp(self):
    self.req_format = 'json'
    self.client = APIClient()

    self.mentor = User.objects.create(username='mentor', first_name='F', last_name='L')

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

    self.timeslot_tier = TimeSlotTier.objects.get(id='wGSj2UozkT')

    TimeSlot.objects.create(room_no=102, timeslot_tier=self.timeslot_tier, workshop=self.workshop)

    workshop_tag1 = WorkshopTag.objects.create(name='tag1')
    workshop_tag2 = WorkshopTag.objects.create(name='tag2')
    self.workshop.tags.add(workshop_tag1, workshop_tag2)

    self.workshop.mentors.add(self.mentor)

    self.req_format = 'json'
    self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.attendee_token.key))

    self.open = AppSettings.objects.get(name=AppSettingName.CDPT_WORKSHOP_REGISTRATION_OPEN.value)
    self.open.value = True
    self.open.save()

  def test_if_exception_raised_when_user_id_and_token_does_not_match_when_getting_list_of_workshops(self):
    resp = self.client.get('/api/users/{}/workshops/'.format(randint(3000, 4000)), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)

    data = resp.data
    self.assertEqual(data['code'], 105)
    self.assertEqual(data['detail'], 'Invalid user ID exception.')

  def test_if_list_of_workshops_matches_schema_if_user_has_no_workshops(self):
    resp = self.client.get('/api/users/{}/workshops/'.format(self.attendee.id), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    jsonschema.validate(resp.data, workshops_json_schema.workshops_list_res_schema)

    workshops = resp.data['workshops']
    self.assertEqual(len(workshops), 0)

  def test_if_list_of_workshops_matches_schema_if_user_has_workshops(self):
    self.workshop.attendees.add(self.attendee)
    resp = self.client.get('/api/users/{}/workshops/'.format(self.attendee.id), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    jsonschema.validate(resp.data, workshops_json_schema.workshops_list_res_schema)

    workshops = resp.data['workshops']
    self.assertEqual(len(workshops), 1)

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
      'workshopId': 123456789
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
      'workshopId': 123456789
    }

    resp = self.client.post('/api/users/{}/workshops/'.format(attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 504)
    self.assertEqual(data['detail'], 'User with ID: {} does not have valid purchase.'.format(attendee.id))

  def test_if_exception_raised_if_user_signs_for_workshop_that_does_not_exist(self):
    payload = {
      'workshopId': 123456789
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
    workshop = Workshop.objects.create(title='t', description='d', max_attendees=0)

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

  def test_if_exception_raised_when_user_id_and_token_does_not_match_when_signing_out_from_workshop(self):
    resp = self.client.delete('/api/users/{}/workshops/{}/'.format(randint(3000, 4000), self.workshop.id), None,
                              format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)

    data = resp.data
    self.assertEqual(data['code'], 105)
    self.assertEqual(data['detail'], 'Invalid user ID exception.')

  def test_if_exception_raised_if_user_signs_out_from_workshop_that_does_not_exist(self):
    workshop_id = '0123456789'
    resp = self.client.delete('/api/users/{}/workshops/{}/'.format(self.attendee.id, workshop_id), None,
                              format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    data = resp.data
    self.assertEqual(data['code'], 501)
    self.assertEqual(data['detail'], 'Workshop with ID: {} not found'.format(workshop_id))

  def test_if_exception_raised_if_user_signs_out_from_workshop_which_it_is_not_an_attendee(self):
    resp = self.client.delete('/api/users/{}/workshops/{}/'.format(self.attendee.id, self.workshop.id), None,
                              format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 509)
    self.assertEqual(data['detail'], 'User with ID: {} is not signed for workshop with ID: {}'.format(self.attendee.id,
                                                                                                      self.workshop.id))

  def test_if_user_successfully_signs_out_from_workshop(self):
    self.workshop.attendees.add(self.attendee)

    self.assertIn(self.attendee, self.workshop.attendees.all())
    self.assertEqual(self.workshop.attendees.count(), 1)

    resp = self.client.delete('/api/users/{}/workshops/{}/'.format(self.attendee.id, self.workshop.id), None,
                              format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)
    self.assertIsNone(resp.data)

    self.assertEqual(self.workshop.attendees.count(), 0)
    self.assertNotIn(self.attendee, self.workshop.attendees.all())

  def test_if_user_successfully_signs_out_from_workshop_and_fails_after(self):
    self.workshop.attendees.add(self.attendee)

    self.assertIn(self.attendee, self.workshop.attendees.all())
    self.assertEqual(self.workshop.attendees.count(), 1)

    resp = self.client.delete('/api/users/{}/workshops/{}/'.format(self.attendee.id, self.workshop.id), None,
                              format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)
    self.assertIsNone(resp.data)

    self.assertEqual(self.workshop.attendees.count(), 0)
    self.assertNotIn(self.attendee, self.workshop.attendees.all())

    resp = self.client.delete('/api/users/{}/workshops/{}/'.format(self.attendee.id, self.workshop.id), None,
                              format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 509)
    self.assertEqual(data['detail'], 'User with ID: {} is not signed for workshop with ID: {}'.format(self.attendee.id,
                                                                                                      self.workshop.id))

    self.assertEqual(self.workshop.attendees.count(), 0)
    self.assertNotIn(self.attendee, self.workshop.attendees.all())

  def test_if_middle_time_slot_layers_are_mutually_exclusive_day_1(self):
    timeslot_tier_2 = TimeSlotTier.objects.get(id='6DNs2lvvZH')
    timeslot_tier_3 = TimeSlotTier.objects.get(id='XurOSgWLtg')

    workshop_2 = Workshop.objects.create(title='W1', description='D1')
    workshop_3 = Workshop.objects.create(title='W2', description='D2')

    TimeSlot.objects.create(room_no=102, timeslot_tier=timeslot_tier_2, workshop=workshop_2)
    TimeSlot.objects.create(room_no=103, timeslot_tier=timeslot_tier_3, workshop=workshop_3)

    workshop_2.attendees.add(self.attendee)

    self.assertEqual(workshop_2.attendees.count(), 1)
    self.assertEqual(workshop_3.attendees.count(), 0)

    payload = {
      'workshopId': workshop_3.id
    }

    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 510)
    self.assertEqual(data['detail'], 'Cannot sign for workshop when tiers are mutually exclusive.')

    self.assertEqual(workshop_2.attendees.count(), 1)
    self.assertEqual(workshop_3.attendees.count(), 0)

  def test_if_middle_time_slot_layers_are_mutually_exclusive_day_2(self):
    timeslot_tier_2 = TimeSlotTier.objects.get(id='VZG2dH6HoX')
    timeslot_tier_3 = TimeSlotTier.objects.get(id='Rf0gaLELyI')

    workshop_2 = Workshop.objects.create(title='W1', description='D1')
    workshop_3 = Workshop.objects.create(title='W2', description='D2')

    TimeSlot.objects.create(room_no=102, timeslot_tier=timeslot_tier_2, workshop=workshop_2)
    TimeSlot.objects.create(room_no=103, timeslot_tier=timeslot_tier_3, workshop=workshop_3)

    workshop_2.attendees.add(self.attendee)

    self.assertEqual(workshop_2.attendees.count(), 1)
    self.assertEqual(workshop_3.attendees.count(), 0)

    payload = {
      'workshopId': workshop_3.id
    }

    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_409_CONFLICT)

    data = resp.data
    self.assertEqual(data['code'], 510)
    self.assertEqual(data['detail'], 'Cannot sign for workshop when tiers are mutually exclusive.')

    self.assertEqual(workshop_2.attendees.count(), 1)
    self.assertEqual(workshop_3.attendees.count(), 0)

  def test_if_all_cross_day_pairs_are_not_mutually_exclusive(self):
    for p in [
      ('6DNs2lvvZH', 'VZG2dH6HoX'),
      ('6DNs2lvvZH', 'Rf0gaLELyI'),
      ('XurOSgWLtg', 'VZG2dH6HoX'),
      ('XurOSgWLtg', 'Rf0gaLELyI')
    ]:
      timeslot_tier_1 = TimeSlotTier.objects.get(id=p[0])
      timeslot_tier_2 = TimeSlotTier.objects.get(id=p[1])

      workshop_2 = Workshop.objects.create(title='W1', description='D1')
      workshop_3 = Workshop.objects.create(title='W2', description='D2')

      TimeSlot.objects.create(room_no='102', timeslot_tier=timeslot_tier_1, workshop=workshop_2)
      TimeSlot.objects.create(room_no='103', timeslot_tier=timeslot_tier_2, workshop=workshop_3)

      workshop_2.attendees.add(self.attendee)

      self.assertEqual(workshop_2.attendees.count(), 1)
      self.assertEqual(workshop_3.attendees.count(), 0)

      payload = {
        'workshopId': workshop_3.id
      }

      resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

      self.assertEqual(resp.status_code, HTTP_204_NO_CONTENT)

      self.assertEqual(workshop_2.attendees.count(), 1)
      self.assertEqual(workshop_3.attendees.count(), 1)

      TimeSlot.objects.all().delete()

      workshop_2.delete()
      workshop_3.delete()

  def test_if_exception_raised_when_registration_closed(self):
    payload = {
      'workshopId': self.workshop.id,
    }
    self.open.value = False
    self.open.save()

    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), payload, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_410_GONE)
    self.assertEqual(resp.data['code'], 402)
    self.assertEqual(resp.data['detail'], 'Workshops registration closed')

  def test_if_exception_raised_when_registering_for_started_workshop(self):
    tier = TimeSlotTier.objects.create(date_from=datetime.datetime.now(), date_to=datetime.datetime.now(), order=0,
                                       day=TimeSlotTierDayName.FIRST.value)
    workshop = Workshop.objects.create(title='t', description='d', max_attendees=5)

    TimeSlot.objects.create(room_no=103, timeslot_tier=tier, workshop=workshop)

    resp = self.client.post('/api/users/{}/workshops/'.format(self.attendee.id), {'workshopId': workshop.id},
                            format=self.req_format)

    self.assertEquals(0, workshop.attendees.count())

    self.assertEqual(resp.status_code, HTTP_410_GONE)

    data = resp.data
    self.assertEqual(data['code'], 511)
    self.assertEqual(data['detail'], 'Workshop with ID: {} has already started.'.format(workshop.id))

    workshop = Workshop.objects.get(id=workshop.id)
    self.assertEquals(0, workshop.attendees.count())

  def test_if_exception_raised_when_unregistering_for_started_workshop(self):
    tier = TimeSlotTier.objects.create(date_from=datetime.datetime.now(), date_to=datetime.datetime.now(), order=0,
                                       day=TimeSlotTierDayName.FIRST.value)
    workshop = Workshop.objects.create(title='t', description='d', max_attendees=5)

    TimeSlot.objects.create(room_no=103, timeslot_tier=tier, workshop=workshop)
    workshop.attendees.add(self.attendee)

    resp = self.client.delete('/api/users/{}/workshops/{}/'.format(self.attendee.id, workshop.id), None,
                              format=self.req_format)

    self.assertEquals(1, workshop.attendees.count())

    self.assertEqual(resp.status_code, HTTP_410_GONE)

    data = resp.data
    self.assertEqual(data['code'], 511)
    self.assertEqual(data['detail'], 'Workshop with ID: {} has already started.'.format(workshop.id))

    workshop = Workshop.objects.get(id=workshop.id)
    self.assertEquals(1, workshop.attendees.count())

  def tearDown(self):
    self.client.credentials(HTTP_AUTHORIZATION=None)
    Workshop.objects.all().delete()
    User.objects.all().delete()
    Purchase.objects.all().delete()
    Product.objects.all().delete()
    PriceTier.objects.all().delete()
