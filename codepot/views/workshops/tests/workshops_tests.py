import datetime

import jsonschema
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.status import HTTP_200_OK
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

    workshop = Workshop.objects.create(
      title='Workshop',
      description='Description with a few words'
    )
    workshop_tag1 = WorkshopTag.objects.create(name='tag1')
    workshop_tag2 = WorkshopTag.objects.create(name='tag2')
    workshop.tags.add(workshop_tag1, workshop_tag2)

    mentor = User.objects.create(first_name='F', last_name='L')
    workshop.mentors.add(mentor)

    timeslot_tier = TimeSlotTier.objects.create(date_from=datetime.datetime.now(), date_to=datetime.datetime.now(),
                                                day=TimeSlotTierDayName.FIRST.value)
    TimeSlot.objects.create(room_no=102, timeslot_tier=timeslot_tier, workshop=workshop)

  def test_if_workshops_not_requires_authorization(self):
    resp = self.client.get('/api/workshops/', None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

  def test_if_list_of_workshops_matches_schema(self):
    client = APIClient()

    resp = client.get('/api/workshops/', None, format=self.req_format)

    self.assertEqual(resp.status_code, HTTP_200_OK)

    jsonschema.validate(resp.data, workshops_json_schema.workshops_list_res_schema)

  def tearDown(self):
    Workshop.objects.all().delete()
    WorkshopTag.objects.all().delete()
    User.objects.all().delete()
    TimeSlot.objects.all().delete()
    TimeSlotTier.objects.all().delete()
