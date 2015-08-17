from haystack.query import SearchQuerySet
import jsonschema
from rest_framework.decorators import (
  api_view,
  permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from codepot.logging import logger
from codepot.models import Workshop
from .__utils import (
  find_workshop_for_id_or_raise,
  prepare_list_of_workshops_response,
)
from codepot.views.workshops import workshops_json_schema
from codepot.views.workshops.exceptions import WorkshopIllegalAccessException


@api_view(['GET', ])
@permission_classes((AllowAny,))
def get_workshops(request, **kwargs):
  workshops = Workshop.objects.all()
  return prepare_list_of_workshops_response(workshops)


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


@api_view(['POST', ])
@permission_classes((AllowAny,))
def search_workshops(request, **kwargs):
  payload = request.DATA

  __validate_search_workshops_payload(payload)

  query = payload['query']

  logger.info('Looking for workshops for query: {}'.format(query))

  workshops = __find_workshops_for_query(query)

  return prepare_list_of_workshops_response(workshops)


def __validate_search_workshops_payload(payload):
  jsonschema.validate(payload, workshops_json_schema.workshop_search_req_schema)


def __find_workshops_for_query(query):
  search_results = SearchQuerySet().models(Workshop).filter(text__in=query.split()).load_all()
  valid_results = [result for result in search_results if result is not None]
  for result in valid_results:
    logger.info('Found result with id: {:<30} and score: {}'.format(result.id, result.score))

  return [search_result.object for search_result in search_results]
