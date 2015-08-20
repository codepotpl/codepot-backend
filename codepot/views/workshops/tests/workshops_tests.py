import datetime

import jsonschema
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.status import (
  HTTP_200_OK,
  HTTP_404_NOT_FOUND,
  HTTP_403_FORBIDDEN,
  HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APIClient

from celerytq.tasks import rebuild_workshops_full_text_search
from codepot.models import (
  Workshop,
  WorkshopTag,
  TimeSlot,
  TimeSlotTier,
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
    self.workshop_tag1 = WorkshopTag.objects.create(name='tag1')
    self.workshop_tag2 = WorkshopTag.objects.create(name='tag2')
    self.workshop.tags.add(self.workshop_tag1, self.workshop_tag2)

    self.mentor = User.objects.create(username='mentor', first_name='MENTOR_FIRST', last_name='MENTOR_LAST')
    self.mentor_token = Token.objects.create(user=self.mentor)

    self.attendee = User.objects.create(username='attendee', first_name='F', last_name='L')
    self.attendee_token = Token.objects.create(user=self.attendee)

    self.workshop.mentors.add(self.mentor)
    self.workshop.attendees.add(self.attendee)

    self.timeslot_tier = TimeSlotTier.objects.get(id='wGSj2UozkT')
    self.timeslot_tier2 = TimeSlotTier.objects.get(id='6DNs2lvvZH')

    TimeSlot.objects.create(room_no=102, timeslot_tier=self.timeslot_tier, workshop=self.workshop)
    TimeSlot.objects.create(room_no=102, timeslot_tier=self.timeslot_tier2, workshop=self.workshop)

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
    workshop_id = int(datetime.datetime.now().timestamp())
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

  def test_if_bad_request_exception_raised_when_empty_search_workshops_request(self):
    resp = self.client.post('/api/workshops/search/', None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    data = resp.data
    self.assertEqual(data['code'], 0)
    self.assertEqual(data['detail'], "'query' is a required property")

  def test_if_bad_request_exception_raised_when_too_short_search_workshops_request(self):
    resp = self.client.post('/api/workshops/search/', {'query': 'aa'}, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    data = resp.data
    self.assertEqual(data['code'], 0)
    self.assertEqual(data['detail'], "'aa' is too short")

  def test_if_empty_list_returned_for_valid_query_and_empty_database(self):
    resp = self.client.post('/api/workshops/search/', {'query': 'aaa'}, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    data = resp.data

    jsonschema.validate(resp.data, workshops_json_schema.workshops_list_res_schema)

    workshops = data['workshops']
    self.assertEqual(len(workshops), 0)

  def test_if_filtering_by_tag_works_correctly(self):
    rebuild_workshops_full_text_search()

    resp = self.client.post('/api/workshops/search/', {'query': 'tag1'}, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    data = resp.data

    jsonschema.validate(resp.data, workshops_json_schema.workshops_list_res_schema)

    workshops = data['workshops']
    self.assertEqual(len(workshops), 1)
    workshop = workshops[0]
    self.assertEqual(workshop['id'], self.workshop.id)

  def test_if_filtering_by_description_works_correctly(self):
    rebuild_workshops_full_text_search()

    resp = self.client.post('/api/workshops/search/', {'query': 'Description with a few words'}, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    data = resp.data

    jsonschema.validate(resp.data, workshops_json_schema.workshops_list_res_schema)

    workshops = data['workshops']
    self.assertEqual(len(workshops), 1)
    workshop = workshops[0]
    self.assertEqual(workshop['id'], self.workshop.id)

  def test_if_filtering_by_tag_mentor_works_correctly(self):
    rebuild_workshops_full_text_search()

    resp = self.client.post('/api/workshops/search/', {'query': self.mentor.last_name}, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    data = resp.data

    jsonschema.validate(resp.data, workshops_json_schema.workshops_list_res_schema)

    workshops = data['workshops']
    self.assertEqual(len(workshops), 1)
    workshop = workshops[0]
    self.assertEqual(workshop['id'], self.workshop.id)

  def test_if_workshop_matching_two_tags_has_better_score_than_workshop_matching_single_tag(self):
    workshop = Workshop.objects.create(
      title='Workshop',
      description='Description with a few words'
    )
    workshop.tags.add(self.workshop_tag1)
    TimeSlot.objects.create(room_no=103, timeslot_tier=self.timeslot_tier, workshop=workshop)
    mentor = User.objects.create(username='mentor2', first_name='MENTOR_FIRST2', last_name='MENTOR_LAST2')
    workshop.mentors.add(mentor)

    rebuild_workshops_full_text_search()

    resp = self.client.post('/api/workshops/search/', {'query': 'tag1 tag2'}, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    data = resp.data

    jsonschema.validate(resp.data, workshops_json_schema.workshops_list_res_schema)

    workshops = data['workshops']
    self.assertEqual(len(workshops), 2)
    self.assertEqual(workshops[0]['id'], self.workshop.id)
    self.assertEqual(workshops[1]['id'], workshop.id)

  def test_if_workshop_timeslots_are_ordered_properly(self):
    client = APIClient()

    resp = client.get('/api/workshops/', None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    jsonschema.validate(resp.data, workshops_json_schema.workshops_list_res_schema)

    timeslots = resp.data['workshops'][0]['timeSlots']
    self.assertEqual(timeslots[0]['order'], 0)
    self.assertEqual(timeslots[0]['room'], '102')
    self.assertEqual(timeslots[1]['order'], 1)
    self.assertEqual(timeslots[1]['room'], '102')

  def test_if_workshop_places_response_matches_schema(self):
    client = APIClient()

    resp = client.post('/api/workshops/places/', None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    jsonschema.validate(resp.data, workshops_json_schema.workshop_places_res_schema)

  def tearDown(self):
    self.client.credentials(HTTP_AUTHORIZATION=None)
    Workshop.objects.all().delete()
    WorkshopTag.objects.all().delete()
    User.objects.all().delete()
    TimeSlot.objects.all().delete()
