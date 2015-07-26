import datetime

import jsonschema
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.status import (
  HTTP_200_OK,
  HTTP_404_NOT_FOUND,
  HTTP_403_FORBIDDEN,
)
from rest_framework.test import APIClient

from codepot.models import (
  Workshop,
  WorkshopTag,
  TimeSlot,
  TimeSlotTier,
  TimeSlotTierDayName,
)
from codepot.views.workshops import workshops_json_schema


class WorkshopsListTests(TestCase):
  def setUp(self):
    self.req_format = 'json'
    self.client = APIClient()

    self.workshop = Workshop.objects.create(
      title='Workshop',
      description='Description with a few words'
    )
    workshop_tag1 = WorkshopTag.objects.create(name='tag1')
    workshop_tag2 = WorkshopTag.objects.create(name='tag2')
    self.workshop.tags.add(workshop_tag1, workshop_tag2)

    self.mentor = User.objects.create(username='mentor', first_name='F', last_name='L')
    self.mentor_token = Token.objects.create(user=self.mentor)

    self.attendee = User.objects.create(username='attendee', first_name='F', last_name='L')
    self.attendee_token = Token.objects.create(user=self.attendee)

    self.workshop.mentors.add(self.mentor)
    self.workshop.attendees.add(self.attendee)

    timeslot_tier = TimeSlotTier.objects.create(date_from=datetime.datetime.now(), date_to=datetime.datetime.now(),
                                                day=TimeSlotTierDayName.FIRST.value)
    TimeSlot.objects.create(room_no=102, timeslot_tier=timeslot_tier, workshop=self.workshop)

  def test_if_workshops_not_requires_authorization(self):
    resp = self.client.get('/api/workshops/', None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

  def test_if_list_of_workshops_matches_schema(self):
    client = APIClient()

    resp = client.get('/api/workshops/', None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    jsonschema.validate(resp.data, workshops_json_schema.workshops_list_res_schema)

  def test_if_not_found_exception_raised_when_fetching_attendees_for_workshop(self):
    self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.mentor_token.key))
    workshop_id = datetime.datetime.now()
    resp = self.client.get('/api/workshops/{}/attendees/'.format(workshop_id), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    data = resp.data
    self.assertEqual(data['code'], 501)
    self.assertEqual(data['detail'], 'Workshop with ID: {} not found'.format(workshop_id))

  def test_if_forbidden_exception_raised_when_non_mentor_tries_to_fetch_attendees(self):
    user = User.objects.create(username='U', first_name='A', last_name='B')
    token = Token.objects.create(user=user)

    self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
    resp = self.client.get('/api/workshops/{}/attendees/'.format(self.workshop.id), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)

    data = resp.data
    self.assertEqual(data['code'], 502)
    self.assertEqual(data['detail'], 'Only mentors are allowed to access workshop attendees list')

  def test_if_attendees_list_returned_for_workshop_mentor(self):
    self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.mentor_token.key))
    resp = self.client.get('/api/workshops/{}/attendees/'.format(self.workshop.id), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    data = resp.data
    attendees = data['attendees']
    self.assertEqual(len(attendees), 1)

    attendee = attendees[0]
    self.assertEqual(len(attendee), 4)
    self.assertEqual(attendee['id'], self.attendee.id)
    self.assertEqual(attendee['firstName'], self.attendee.first_name)
    self.assertEqual(attendee['lastName'], self.attendee.last_name)
    self.assertEqual(attendee['email'], self.attendee.email)

  def tearDown(self):
    self.client.credentials(HTTP_AUTHORIZATION=None)
    Workshop.objects.all().delete()
    WorkshopTag.objects.all().delete()
    User.objects.all().delete()
    TimeSlot.objects.all().delete()
    TimeSlotTier.objects.all().delete()
