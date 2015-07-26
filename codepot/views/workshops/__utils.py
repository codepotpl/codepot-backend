from codepot.logging import logger
from codepot.models import Workshop
from codepot.views.workshops import WorkshopNotFoundException
from codepot.views.workshops.exceptions import WorkshopIllegalAccessException


def find_workshop_for_id_or_raise(workshop_id):
  try:
    return Workshop.objects.get(id=workshop_id)
  except Workshop.DoesNotExist as e:
    logger.error('No workshops found for ID: {}, err: {}'.format(workshop_id, str(e)))
    raise WorkshopNotFoundException(workshop_id)


def check_if_user_is_workshop_mentor_or_attendee(workshop, user):
  if (user not in workshop.attendees.all()) and (user not in workshop.mentors.all()):
    logger.error('User with ID: {} tried to access workshop with ID: {} illegally.'.format(user.id, workshop.id))
    raise WorkshopIllegalAccessException('Only mentors and attendees are allowed to access workshop data')
