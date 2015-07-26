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
