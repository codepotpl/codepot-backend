import jsonschema
from django.db import transaction
from rest_framework.decorators import (
  api_view,
  permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
  HTTP_204_NO_CONTENT,
)

from codepot.exceptions import WorkshopsRegistrationClosedException
from codepot.logging import logger
from codepot.models import (
  Purchase,
  PaymentStatusName,
  TimeSlot,
  AppSettings,
)
from codepot.models.workshops import Workshop
from codepot.views.users import _compare_ids_and_raise_exception_if_different
from codepot.views.workshops import workshops_json_schema
from codepot.views.workshops.__utils import (
  find_workshop_for_id_or_raise,
  prepare_list_of_workshops_response,
)
from codepot.views.workshops.exceptions import (
  WorkshopWithoutPurchaseSignAttemptException,
  UserAlreadySignedForWorkshopException,
  MentorCannotSignForOwnWorkshopException,
  WorkshopMaxAttendeesLimitExceededException,
  UserAlreadySignedForWorkshopInTierException,
  UserNotSignedForWorkshopException, MutuallyExclusiveTiersException)

__mutually_exclusive_tiers_ids_day_1 = set(['6DNs2lvvZH', 'XurOSgWLtg', ])
__mutually_exclusive_tiers_ids_day_2 = set(['VZG2dH6HoX', 'Rf0gaLELyI', ])

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
  workshops = Workshop.objects.filter(attendees__in=[user])

  return prepare_list_of_workshops_response(workshops)

def _sign_user_for_workshop(user, payload):
  __check_if_workshops_registration_is_open()

  __validate_sign_for_workshop_payload(payload)

  workshop_id = payload['workshopId']

  __check_if_user_has_successful_purchase(user, workshop_id)

  workshop = find_workshop_for_id_or_raise(workshop_id)

  __check_if_user_already_signed_for_workshop(user, workshop)

  __check_if_user_is_workshop_mentor(user, workshop)

  __check_if_workshop_attendees_limit_exceeded(workshop)

  __check_if_user_already_signed_for_workshop_in_current_slot_tier(user, workshop)

  __check_if_timeslot_layers_are_not_mutually_exclusive(user, workshop)

  __add_user_to_workshop_attendees(workshop, user)

  return Response(status=HTTP_204_NO_CONTENT)


def __check_if_workshops_registration_is_open():
  if not AppSettings.objects.is_workshop_registration_open():
    raise WorkshopsRegistrationClosedException()

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
  user_timeslots = __get_user_timeslots(user)
  user_tiers = __get_timeslot_tiers(user_timeslots)

  workshop_timeslots = __get_workshop_timeslots(workshop)
  workshop_tiers = __get_timeslot_tiers(workshop_timeslots)

  intersection = user_tiers.intersection(workshop_tiers)

  if intersection:
    msg = 'User with ID: {}, is already registered for workshop in tier(s): {}.'.format(user.id, intersection)
    logger.error(msg)
    raise UserAlreadySignedForWorkshopInTierException(msg)


def __check_if_timeslot_layers_are_not_mutually_exclusive(user, workshop):
  workshop_timeslots = __get_workshop_timeslots(workshop)
  workshop_tiers = __get_timeslot_tiers(workshop_timeslots)
  workshop_tiers_ids = __get_timeslot_tiers_ids(workshop_tiers)

  if not (workshop_tiers_ids & (__mutually_exclusive_tiers_ids_day_1 | __mutually_exclusive_tiers_ids_day_2)):
    return

  user_timeslots = __get_user_timeslots(user)
  user_tiers = __get_timeslot_tiers(user_timeslots)
  user_tiers_ids = __get_timeslot_tiers_ids(user_tiers)

  if (workshop_tiers_ids & __mutually_exclusive_tiers_ids_day_1) and \
      (user_tiers_ids & __mutually_exclusive_tiers_ids_day_1):
    __raise_mutually_exclusive_tiers_exceptions(user, workshop, user_tiers_ids, workshop_tiers_ids)

  if (workshop_tiers_ids & __mutually_exclusive_tiers_ids_day_2) and \
      (user_tiers_ids & __mutually_exclusive_tiers_ids_day_2):
    __raise_mutually_exclusive_tiers_exceptions(user, workshop, user_tiers_ids, workshop_tiers_ids)


def __get_user_timeslots(user):
  return TimeSlot.objects.filter(workshop__in=user.attendees.all())


def __get_workshop_timeslots(workshop):
  return workshop.timeslot_set.all()


def __get_timeslot_tiers(timeslots):
  return set([ts.timeslot_tier for ts in timeslots])


def __get_timeslot_tiers_ids(timeslot_tiers):
  return set([tst.id for tst in timeslot_tiers])


def __raise_mutually_exclusive_tiers_exceptions(user, workshop, user_tiers_ids, workshop_tiers_ids):
  logger.error(
    'User with ID: {} cannot sign for workshop with ID: {}. Mutually exclusive tiers, users: {}, workshops :{}.'
      .format(user.id, workshop.id, user_tiers_ids, workshop_tiers_ids)
  )
  raise MutuallyExclusiveTiersException()

def __add_user_to_workshop_attendees(workshop, user):
  workshop.attendees.add(user)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
@transaction.atomic()
def delete_user_workshop(request, **kwargs):
  user = request.user
  user_id = kwargs['user_id']

  _compare_ids_and_raise_exception_if_different(user_id, user.id)

  workshop_id = kwargs['workshop_id']

  workshop = find_workshop_for_id_or_raise(workshop_id)

  __check_if_user_is_not_workshop_attendee(workshop, user)

  workshop.attendees.remove(user)

  return Response(status=HTTP_204_NO_CONTENT)


def __check_if_user_is_not_workshop_attendee(workshop, user):
  if user not in workshop.attendees.all():
    raise UserNotSignedForWorkshopException(user.id, workshop.id)
