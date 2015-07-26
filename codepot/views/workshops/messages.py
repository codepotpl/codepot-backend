from rest_framework.decorators import (
  api_view,
  permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from .__utils import (
  find_workshop_for_id_or_raise,
  check_if_user_is_workshop_mentor_or_attendee,
)


@api_view(['GET', 'POST', ])
@permission_classes((IsAuthenticated,))
def list_or_create_workshop_message(request, **kwargs):
  workshop_id = kwargs['workshop_id']
  workshop = find_workshop_for_id_or_raise(workshop_id)

  user = request.user
  check_if_user_is_workshop_mentor_or_attendee(workshop, user)

  method = request.method
  if method == 'GET':
    return _get_messages(workshop)
  elif method == 'POST':
    return _create_new_message(request, kwargs)
  else:
    raise Exception('Should never happen! Method: {}'.format(method))


def _get_messages(workshop):
  return Response(
    data={
      'messages': [
        {
          'id': m.id,
          'author': '{} {}'.format(m.author.first_name, m.author.last_name),
          'content': m.message,
          'created': m.created,
        } for m in workshop.workshopmessage_set.all()
        ]
    },
    status=HTTP_200_OK
  )


def _create_new_message(request, kwargs):
  pass


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def delete_workshop_message(request, **kwargs):
  return Response(
    data={'method': request.method, 'workshopId': kwargs['workshop_id'], 'messageId': kwargs['message_id']})
