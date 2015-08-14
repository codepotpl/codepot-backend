import json
import sys
from optparse import make_option

from django.contrib.auth.models import User

from django.core.management.base import BaseCommand

from codepot.models import (
  Workshop,
  WorkshopTag,
  TimeSlot,
  TimeSlotTier,
  TimeSlotTierDayName,
)


class Command(BaseCommand):
  option_list = (
    make_option(
      '-f', '--file',
      dest='workshops_json',
      help='Path to file with workshops JSON data'
    ),
  )
  friday_tiers = list(TimeSlotTier.objects.filter(day=TimeSlotTierDayName.FIRST.value).order_by('date_from'))
  saturday_tiers = list(TimeSlotTier.objects.filter(day=TimeSlotTierDayName.SECOND.value).order_by('date_from'))

  def _create_workshop(self, entry):
    return Workshop.objects.create(
      title=entry['title'],
      description=entry['descriptionInMd'],
      max_attendees=entry['capacity']
    )

  def _add_workshop_tags(self, workshop, entry):
    if entry.get('tags'):
      workshop.tags.add(*[WorkshopTag.objects.get_or_create(name=t)[0] for t in entry['tags']])

  def _add_mentors(self, workshop, entry):
    if entry.get('tutorEmails'):
      workshop.mentors.add(*[User.objects.get(email=email) for email in entry['tutorEmails']])

  def _create_time_slots(self, workshop, entry):
    tiers = None
    day = entry['day']
    if day == 'FRIDAY':
      tiers = self.friday_tiers

    if day == 'SATURDAY':
      tiers = self.saturday_tiers

    for tier in entry['timetire']:
      TimeSlot.objects.create(room_no=entry['room'], timeslot_tier=tiers[tier - 1], workshop=workshop)

  def handle(self, *args, **options):
    workshops_json = options.get('workshops_json')

    if workshops_json is None:
      self.stderr.write('No mentors JSON file passed.')
      sys.exit(1)

    self.stdout.write("Loading data from: '{}' file".format(workshops_json))

    with open(workshops_json) as file:
      data = json.load(file)

      Workshop.objects.all().delete()
      WorkshopTag.objects.all().delete()

      for entry in data:
        try:
          workshop = self._create_workshop(entry)
          self._add_workshop_tags(workshop, entry)
          self._add_mentors(workshop, entry)
          self._create_time_slots(workshop, entry)

        except Exception as e:
          self.stderr.write('Error why adding workshop: {}, err: {}'.format(entry['title'], e))
