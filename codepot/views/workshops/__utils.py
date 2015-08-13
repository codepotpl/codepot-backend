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
      'workshops': [
        {
          'id': w.id,
          'title': w.title,
          'description': w.description,
          'timeSlots': [
            {
              'id': ts.id,
              'day': ts.timeslot_tier.day,
              'startTime': ts.timeslot_tier.date_from.isoformat(),
              'endTime': ts.timeslot_tier.date_to.isoformat(),
              'room': ts.room_no,
              'order': ts.timeslot_tier.order,
            } for ts in sorted(w.timeslot_set.all(), key=lambda x: x.timeslot_tier.date_from)
            ],
          'mentors': [
            {
              'id': m.id,
              'firstName': m.first_name,
              'lastName': m.last_name,
            } for m in w.mentors.all()
            ],
          'tags': [
            {
              'id': t.name,
              'name': t.name,
            } for t in w.tags.all()
            ],
        } for w in workshops
        ]
    },
    HTTP_200_OK
  )
