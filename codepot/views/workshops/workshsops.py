from rest_framework.decorators import (
  api_view,
  permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from codepot.logging import logger
from codepot.models import Workshop
from .__utils import find_workshop_for_id_or_raise
from codepot.views.workshops.exceptions import WorkshopIllegalAccessException


@api_view(['GET', ])
@permission_classes((AllowAny,))
def get_workshops(request, **kwargs):
  workshops = Workshop.objects.all()

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
            } for ts in w.timeslot_set.all()
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

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_workshop_attendees(request, **kwargs):
  workshop_id = kwargs['workshop_id']
  workshop = find_workshop_for_id_or_raise(workshop_id)

  user = request.user

  _check_if_user_is_workshop_mentor(workshop, user)

  return Response(
    data={
      'attendees': [
        {
          'id': a.id,
          'firstName': a.first_name,
          'lastName': a.last_name,
          'email': a.email,
        } for a in workshop.attendees.all()
        ]
    },
    status=HTTP_200_OK
  )

def _check_if_user_is_workshop_mentor(workshop, user):
  if user not in workshop.mentors.all():
    logger.error(
      'User with ID: {} tried to access attendees list for workshop with ID: {}'.format(user.id, workshop.id))
    raise WorkshopIllegalAccessException('Only mentors are allowed to access workshop attendees list')
