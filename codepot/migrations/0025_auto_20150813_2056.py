# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import pytz
from django.db import migrations

from codepot.models import TimeSlotTierDayName

warsaw_tz = pytz.timezone('Europe/Warsaw')


def initial_data(apps, schema_editor):
  TimeSlotTier = apps.get_model('codepot', 'TimeSlotTier')
  TimeSlotTier.objects.all().delete()

  TimeSlotTier.objects.create(
    id='wGSj2UozkT',
    date_from=warsaw_tz.localize(datetime(2015, 8, 29, 9, 15, 0)),
    date_to=warsaw_tz.localize(datetime(2015, 8, 29, 12, 30, 0)),
    day=TimeSlotTierDayName.FIRST.value,
    order=0
  )

  TimeSlotTier.objects.create(
    id='6DNs2lvvZH',
    date_from=warsaw_tz.localize(datetime(2015, 8, 29, 12, 45, 0)),
    date_to=warsaw_tz.localize(datetime(2015, 8, 29, 13, 45, 0)),
    day=TimeSlotTierDayName.FIRST.value,
    order=1
  )

  TimeSlotTier.objects.create(
    id='XurOSgWLtg',
    date_from=warsaw_tz.localize(datetime(2015, 8, 29, 13, 45, 0)),
    date_to=warsaw_tz.localize(datetime(2015, 8, 29, 14, 45, 0)),
    day=TimeSlotTierDayName.FIRST.value,
    order=2
  )

  TimeSlotTier.objects.create(
    id='xMPbefCHK6',
    date_from=warsaw_tz.localize(datetime(2015, 8, 29, 15, 0, 0)),
    date_to=warsaw_tz.localize(datetime(2015, 8, 29, 18, 15, 0)),
    day=TimeSlotTierDayName.FIRST.value,
    order=3
  )

  TimeSlotTier.objects.create(
    id='sCbIKF07yh',
    date_from=warsaw_tz.localize(datetime(2015, 8, 30, 9, 30, 0)),
    date_to=warsaw_tz.localize(datetime(2015, 8, 30, 12, 45, 0)),
    day=TimeSlotTierDayName.SECOND.value,
    order=0
  )

  TimeSlotTier.objects.create(
    id='VZG2dH6HoX',
    date_from=warsaw_tz.localize(datetime(2015, 8, 30, 13, 0, 0)),
    date_to=warsaw_tz.localize(datetime(2015, 8, 30, 14, 0, 0)),
    day=TimeSlotTierDayName.SECOND.value,
    order=1
  )

  TimeSlotTier.objects.create(
    id='Rf0gaLELyI',
    date_from=warsaw_tz.localize(datetime(2015, 8, 30, 14, 0, 0)),
    date_to=warsaw_tz.localize(datetime(2015, 8, 30, 15, 0, 0)),
    day=TimeSlotTierDayName.SECOND.value,
    order=2
  )

  TimeSlotTier.objects.create(
    id='QvzUYBHB98',
    date_from=warsaw_tz.localize(datetime(2015, 8, 30, 15, 15, 0)),
    date_to=warsaw_tz.localize(datetime(2015, 8, 30, 18, 30, 0)),
    day=TimeSlotTierDayName.SECOND.value,
    order=3
  )


def remove_data(apps, schema_editor):
  TimeSlotTier = apps.get_model('codepot', 'TimeSlotTier')
  TimeSlotTier.objects.all().delete()


class Migration(migrations.Migration):
  dependencies = [
    ('codepot', '0024_timeslottier_order'),
  ]

  operations = [
    migrations.RunPython(initial_data, reverse_code=remove_data)
  ]
