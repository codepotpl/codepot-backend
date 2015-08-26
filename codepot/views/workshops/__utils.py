from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from codepot.logging import logger
from codepot.models import (
  Workshop,
  WorkshopMessage,
)
from codepot.views.workshops.exceptions import (
  WorkshopNotFoundException,
  WorkshopIllegalAccessException,
  WorkshopMessageNotFoundException,
)


def find_workshop_for_id_or_raise(workshop_id):
  try:
    return Workshop.objects.get(id=workshop_id)
  except Workshop.DoesNotExist as e:
    logger.error('No workshops found for ID: {}, err: {}'.format(workshop_id, str(e)))
    raise WorkshopNotFoundException(workshop_id)


def find_message_for_id_or_raise(message_id):
  try:
    return WorkshopMessage.objects.get(id=message_id)
  except WorkshopMessage.DoesNotExist as e:
    logger.error('No workshop message found for ID: {}, err: {}'.format(message_id, str(e)))
    raise WorkshopMessageNotFoundException(message_id)


def check_if_user_is_workshop_mentor_or_attendee(workshop, user):
  if (user not in workshop.attendees.all()) and (user not in workshop.mentors.all()):
    logger.error('User with ID: {} tried to access workshop with ID: {} illegally.'.format(user.id, workshop.id))
    raise WorkshopIllegalAccessException('Only mentors and attendees are allowed to access workshop data')


def prepare_list_of_workshops_response(workshops):
  return Response(
    {
      'workshops': [map_single_workshop(w) for w in workshops]
    },
    HTTP_200_OK,
    headers={'Cache-Control': 'no-cache, no-store, must-revalidate'}
  )


def map_single_workshop(workshop):
  return {
    'id': workshop.id,
    'title': workshop.title,
    'description': workshop.description,
    'maxAttendees': workshop.max_attendees,
    'attendeesCount': workshop.attendees.count(),
    'timeSlots': [
      {
        'id': ts.id,
        'day': ts.timeslot_tier.day,
        'startTime': ts.timeslot_tier.date_from.isoformat(),
        'endTime': ts.timeslot_tier.date_to.isoformat(),
        'room': ts.room_no,
        'order': ts.timeslot_tier.order,
      } for ts in sorted(workshop.timeslot_set.all(), key=lambda x: x.timeslot_tier.order)
      ],
    'mentors': [__get_workshop_mentor_data(m) for m in workshop.mentors.all()],
    'tags': [
      {
        'id': t.name,
        'name': t.name,
      } for t in workshop.tags.all()
      ],
  }

def sort_workshops_by_start_date(workshops):
  return sorted(workshops, key=lambda x: x.timeslot_set.all()[0].timeslot_tier.date_from)

def __get_workshop_mentor_data(mentor):
  basic_data = {
    'id': mentor.id,
    'firstName': mentor.first_name,
    'lastName': mentor.last_name,
  }
  extended_data = __get_workshop_mentor_extended_data(mentor)
  basic_data.update(extended_data)
  return basic_data


def __get_workshop_mentor_extended_data(mentor):
  workshop_mentor = mentor.workshopmentor if hasattr(mentor, 'workshopmentor') else None
  return {
    'tagline': workshop_mentor.tagline if workshop_mentor else None,
    'pictureURL': workshop_mentor.picture_url if workshop_mentor else None,
    'twitterUsername': workshop_mentor.twitter_username if workshop_mentor else None,
    'githubUsername': workshop_mentor.github_username if workshop_mentor else None,
    'linkedinProfileURL': workshop_mentor.linkedin_profile_url if workshop_mentor else None,
    'stackoverflowId': workshop_mentor.stackoverflow_id if workshop_mentor else None,
    'googleplusHandler': workshop_mentor.googleplus_handler if workshop_mentor else None,
    'websiteURL': workshop_mentor.website_url if workshop_mentor else None,
    'bioInMd': workshop_mentor.bio_in_md if workshop_mentor else None,
  }
