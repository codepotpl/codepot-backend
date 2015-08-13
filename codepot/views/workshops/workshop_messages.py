from django.db import transaction
import jsonschema

from rest_framework.decorators import (
  api_view,
  permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
  HTTP_200_OK,
  HTTP_204_NO_CONTENT,
  HTTP_201_CREATED,
)

from .__utils import (
  find_workshop_for_id_or_raise,
  find_message_for_id_or_raise,
  check_if_user_is_workshop_mentor_or_attendee,
)
from codepot.logging import logger
from codepot.models.workshops import WorkshopMessage
from codepot.views.workshops import workshops_json_schema
from codepot.views.workshops.exceptions import WorkshopIllegalAccessException


@api_view(['GET', 'POST', ])
@permission_classes((IsAuthenticated,))
@transaction.atomic()
def list_or_create_workshop_message(request, **kwargs):
  workshop_id = kwargs['workshop_id']
  workshop = find_workshop_for_id_or_raise(workshop_id)

  user = request.user
  check_if_user_is_workshop_mentor_or_attendee(workshop, user)

  method = request.method
  if method == 'GET':
    return _get_messages(workshop)
  elif method == 'POST':
    return _create_new_message(workshop, user, request.DATA)
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
          'created': m.created.isoformat(),
        } for m in workshop.workshopmessage_set.all()
        ]
    },
    status=HTTP_200_OK
  )


def _create_new_message(workshop, user, payload):
  jsonschema.validate(payload, workshops_json_schema.workshop_message_req_schema)

  message = WorkshopMessage.objects.create(
    workshop=workshop,
    author=user,
    message=payload['content']
  )

  return Response(
    data={
      'message': {
        'id': message.id,
        'author': '{} {}'.format(message.author.first_name, message.author.last_name),
        'content': message.message,
        'created': message.created.isoformat(),
      },
    },
    status=HTTP_201_CREATED
  )


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
@transaction.atomic()
def delete_workshop_message(request, **kwargs):
  workshop_id = kwargs['workshop_id']
  find_workshop_for_id_or_raise(workshop_id)

  message_id = kwargs['message_id']
  message = find_message_for_id_or_raise(message_id)

  user = request.user

  _check_if_user_is_author_of_message_or_workshop_mentor(message, user)

  logger.info('User with ID: {}, deletes messages with ID: {}'.format(user.id, message.id))

  message.delete()

  return Response(status=HTTP_204_NO_CONTENT)


def _check_if_user_is_author_of_message_or_workshop_mentor(message, user):
  author = message.author
  mentors = message.workshop.mentors.all()

  if (user != author) and (user not in mentors):
    logger.error('User with ID: {} tried to delete message with ID: {}'.format(user.id, message.id))
    raise WorkshopIllegalAccessException('Only mentor or author can delete workshop message')
