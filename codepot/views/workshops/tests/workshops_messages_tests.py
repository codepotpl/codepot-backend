import datetime

from django.contrib.auth.models import User
from django.test import TestCase
import jsonschema
from rest_framework.authtoken.models import Token
from rest_framework.status import (
  HTTP_404_NOT_FOUND,
  HTTP_403_FORBIDDEN,
  HTTP_200_OK,
  HTTP_400_BAD_REQUEST)
from rest_framework.test import APIClient

from codepot.models import (
  Workshop,
  WorkshopTag,
  WorkshopMessage,
)
from codepot.views.workshops import workshops_json_schema


class WorkshopsMessagesTests(TestCase):
  def setUp(self):
    self.req_format = 'json'
    self.client = APIClient()

    self.attendee = User.objects.create(username='a', first_name='FA', last_name='LA')
    self.mentor = User.objects.create(username='m', first_name='FM', last_name='LM')
    self.attendee_token = Token.objects.create(user=self.attendee)
    self.mentor_token = Token.objects.create(user=self.mentor)
    self.req_format = 'json'
    self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.attendee_token.key))

    self.workshop = Workshop.objects.create(
      title='Workshop',
      description='Description with a few words'
    )
    self.workshop.attendees.add(self.attendee)
    self.workshop.mentors.add(self.mentor)

    self.workshop_message = WorkshopMessage.objects.create(
      workshop=self.workshop,
      author=self.attendee,
      message='Sample message'
    )

  def test_if_not_found_exception_raised_when_fetching_messages_for_non_existing_workshop(self):
    self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.attendee_token.key))
    workshop_id = datetime.datetime.now()
    resp = self.client.get('/api/workshops/{}/messages/'.format(workshop_id), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    data = resp.data
    self.assertEqual(data['code'], 501)
    self.assertEqual(data['detail'], 'Workshop with ID: {} not found'.format(workshop_id))

  def test_if_forbidden_exception_raised_when_not_mentor_nor_attendee_sends_fetches_workshop_messages(self):
    client = APIClient()
    user = User.objects.create(username='u2', first_name='F', last_name='L')
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))

    resp = client.get('/api/workshops/{}/messages/'.format(self.workshop.id), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)

    data = resp.data
    self.assertEqual(data['code'], 502)
    self.assertEqual(data['detail'], 'Only mentors and attendees are allowed to access workshop data')

  def test_if_workshop_messages_list_returned_correctly_for_both_mentor_and_attendee(self):
    for token in [self.attendee_token, self.mentor_token]:
      self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
      resp = self.client.get('/api/workshops/{}/messages/'.format(self.workshop.id), None, format=self.req_format)

      self.assertEqual(resp.status_code, HTTP_200_OK)

      data = resp.data

      messages = data['messages']
      self.assertEqual(len(messages), 1)

      message = messages[0]
      self.assertEqual(message['id'], self.workshop_message.id)
      self.assertEqual(message['author'], 'FA LA')
      self.assertEqual(message['content'], self.workshop_message.message)
      self.assertIn('created', message)
      self.assertIsNotNone(message['created'])

      jsonschema.validate(message, workshops_json_schema.workshop_message_res_schema)

  def test_if_forbidden_exception_raised_when_not_mentor_nor_attendee_posts_new_workshop_messages(self):
    client = APIClient()
    user = User.objects.create(username='u2', first_name='F', last_name='L')
    token = Token.objects.create(user=user)
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))

    resp = client.post('/api/workshops/{}/messages/'.format(self.workshop.id), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_403_FORBIDDEN)

    data = resp.data
    self.assertEqual(data['code'], 502)
    self.assertEqual(data['detail'], 'Only mentors and attendees are allowed to access workshop data')

  def test_if_not_found_exception_raised_when_creating_message_for_non_existing_workshop(self):
    workshop_id = datetime.datetime.now()
    resp = self.client.post('/api/workshops/{}/messages/'.format(workshop_id), None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    data = resp.data
    self.assertEqual(data['code'], 501)
    self.assertEqual(data['detail'], 'Workshop with ID: {} not found'.format(workshop_id))

  def test_if_both_mentor_and_attendee_can_add_new_message(self):
    self.assertEqual(WorkshopMessage.objects.count(), 1)

    for idx, token in enumerate([self.attendee_token, self.mentor_token]):
      self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
      body = {'content': 'New message: {}'.format(idx)}
      resp = self.client.post('/api/workshops/{}/messages/'.format(self.workshop.id), body, format=self.req_format)

      self.assertEqual(resp.status_code, HTTP_200_OK)

      data = resp.data

      message = data['message']

      self.assertIsNotNone(message['id'])
      self.assertEqual(message['author'], '{} {}'.format(token.user.first_name, token.user.last_name))
      self.assertEqual(message['content'], body['content'])
      self.assertIn('created', message)
      self.assertIsNotNone(message['created'])

      jsonschema.validate(message, workshops_json_schema.workshop_message_res_schema)

    self.assertEqual(WorkshopMessage.objects.count(), 3)

  def test_if_validation_fails_when_invalid_body_send_when_creating_new_workshop_message(self):
    self.assertEqual(WorkshopMessage.objects.count(), 1)

    for idx, token in enumerate([self.attendee_token, self.mentor_token]):
      self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
      body = {'failed_content': 'New message: {}'.format(idx)}
      resp = self.client.post('/api/workshops/{}/messages/'.format(self.workshop.id), body, format=self.req_format)

      self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    self.assertEqual(WorkshopMessage.objects.count(), 1)


  def tearDown(self):
    self.client.credentials(HTTP_AUTHORIZATION=None)
    Workshop.objects.all().delete()
    WorkshopMessage.objects.all().delete()
    WorkshopTag.objects.all().delete()
    User.objects.all().delete()
