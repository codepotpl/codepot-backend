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
)

from codepot.logging import logger
from codepot.models import (
  Purchase,
  PaymentStatusName,
  TimeSlot,
)
from codepot.views.users import _compare_ids_and_raise_exception_if_different
from codepot.views.workshops import workshops_json_schema
from codepot.views.workshops.__utils import find_workshop_for_id_or_raise
from codepot.views.workshops.exceptions import (
  WorkshopWithoutPurchaseSignAttemptException,
  UserAlreadySignedForWorkshopException,
  MentorCannotSignForOwnWorkshopException,
  WorkshopMaxAttendeesLimitExceededException,
  UserAlreadySignedForWorkshopInTierException,
)


@api_view(['GET', 'POST', ])
@permission_classes((IsAuthenticated,))
@transaction.atomic()
def list_user_workshops_or_sign_for_workshops(request, **kwargs):
  user = request.user
  user_id = kwargs['user_id']

  _compare_ids_and_raise_exception_if_different(user_id, user.id)

  method = request.method
  if method == 'GET':
    return _get_user_workshops(user)
  elif method == 'POST':
    payload = request.DATA
    return _sign_user_for_workshop(user, payload)
  else:
    raise Exception('Should never happen! Method: {}'.format(method))


def _get_user_workshops(user):
  return Response(status=HTTP_200_OK)


def _sign_user_for_workshop(user, payload):
  __validate_sign_for_workshop_payload(payload)

  workshop_id = payload['workshopId']

  __check_if_user_has_successful_purchase(user, workshop_id)

  workshop = find_workshop_for_id_or_raise(workshop_id)

  __check_if_user_already_signed_for_workshop(user, workshop)

  __check_if_user_is_workshop_mentor(user, workshop)

  __check_if_workshop_attendees_limit_exceeded(workshop)

  __check_if_user_already_signed_for_workshop_in_current_slot_tier(user, workshop)

  __add_user_to_workshop_attendees(workshop, user)

  return Response(status=HTTP_204_NO_CONTENT)


def __validate_sign_for_workshop_payload(payload):
  jsonschema.validate(payload, workshops_json_schema.sign_for_workshop_req_schema)


def __check_if_user_has_successful_purchase(user, workshop_id):
  try:
    return Purchase.objects.get(user=user, payment_status=PaymentStatusName.SUCCESS.value)
  except Purchase.DoesNotExist as e:
    logger.error(
      'No purchase found for user with ID: {} when signing for workshop with ID: {}, err: {}'.format(
        user.id,
        workshop_id,
        str(e))
    )
    try:
      purchase = Purchase.objects.get(user=user)
      logger.info('User with ID: {} has purchase with ID: {}, status: {}, payment type: {}'.format(
        user.id, purchase.id, purchase.payment_status, purchase.payment_type)
      )
    except Purchase.DoesNotExist:
      pass

    raise WorkshopWithoutPurchaseSignAttemptException(user.id)


def __check_if_user_already_signed_for_workshop(user, workshop):
  if user in workshop.attendees.all():
    raise UserAlreadySignedForWorkshopException(user.id, workshop.id)


def __check_if_user_is_workshop_mentor(user, workshop):
  if user in workshop.mentors.all():
    raise MentorCannotSignForOwnWorkshopException(user.id, workshop.id)


def __check_if_workshop_attendees_limit_exceeded(workshop):
  if workshop.attendees.count() + 1 > workshop.max_attendees:
    raise WorkshopMaxAttendeesLimitExceededException(workshop)


def __check_if_user_already_signed_for_workshop_in_current_slot_tier(user, workshop):
  user_timeslots = TimeSlot.objects.filter(workshop__in=user.attendees.all())
  user_tiers = set([ts.timeslot_tier for ts in user_timeslots])

  workshop_timeslots = workshop.timeslot_set.all()
  workshop_tiers = set([ts.timeslot_tier for ts in workshop_timeslots])

  intersection = user_tiers.intersection(workshop_tiers)

  if intersection:
    msg = 'User with ID: {}, is already registered for workshop in tier(s): {}.'.format(user.id, intersection)
    logger.error(msg)
    raise UserAlreadySignedForWorkshopInTierException(msg)


def __add_user_to_workshop_attendees(workshop, user):
  workshop.attendees.add(user)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
@transaction.atomic()
def delete_user_workshop(request, **kwargs):
  user = request.user
  user_id = kwargs['user_id']

  return Response(status=HTTP_204_NO_CONTENT)
