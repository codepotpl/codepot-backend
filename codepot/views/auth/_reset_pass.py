from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.decorators import (
  api_view,
  parser_classes,
)
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from codepot.logging import logger
from codepot.models import ResetPassword
from codepot.utils import get_rendered_template
from codepot.views import parser_class_for_schema, validate_payload_with_schema
from codepot.views.auth.auth_json_schema import (
  reset_pass_initialize_req_schema,
  reset_pass_finalize_req_schema,
)
from codepot.views.auth.exceptions import (
  UserNotFoundForPasswordResetException,
  ResetPasswordNotFoundException,
)
from celerytq.tasks import send_mail


@api_view(['POST', ])
@permission_classes((AllowAny,))
@parser_classes((parser_class_for_schema(reset_pass_initialize_req_schema),))
@transaction.atomic()
def reset_pass_initialize(request, **kwargs):
  payload = request.DATA

  validate_payload_with_schema(payload, reset_pass_initialize_req_schema)

  email = payload['email']

  logger.info('Starting reset password process for: {}'.format(email))

  user = __find_user_auth_for_email(email)

  if user is not None:
    __remove_previous_reset_pw_attempts(email)
    reset_pw = __create_new_reset_password(email)
    reset_pw_link = __prepare_reset_pw_link(reset_pw.token)

    __send_reset_pw_email(email, reset_pw_link)

  return Response(status=HTTP_204_NO_CONTENT)


def __find_user_auth_for_email(email):
  try:
    return User.objects.get(email=email.lower())
  except User.DoesNotExist:
    logger.error('No user found for email: {}'.format(email))
    return None

def __remove_previous_reset_pw_attempts(email):
  ResetPassword.objects.filter(email=email).delete()


def __create_new_reset_password(email):
  return ResetPassword.objects.create(
    email=email.lower(),
    active=True
  )


def __prepare_reset_pw_link(token):
  return '{}reset-password/{}/'.format(settings.WEB_CLIENT_ADDRESS, token)


def __send_reset_pw_email(email, reset_link):
  send_mail.delay(email, 'Codepot Password Reset.',
                  get_rendered_template('mail/reset_password_initialize.txt', {
                    'resetPasswordLink': reset_link
                  }),
                  get_rendered_template('mail/reset_password_initialize.html', {
                    'resetPasswordLink': reset_link
                  }),
                  ['tickets@codepot.pl']
                  )


@api_view(['POST', ])
@permission_classes((AllowAny,))
@parser_classes((parser_class_for_schema(reset_pass_finalize_req_schema),))
@transaction.atomic()
def reset_pass_finalize(request, **kwargs):
  payload = request.DATA

  validate_payload_with_schema(payload, reset_pass_finalize_req_schema)

  token = payload['token']
  password = payload['password']

  reset_pw = __find_reset_password_attempt(token)
  user = __find_user_for_email(reset_pw.email)

  user.set_password(password)
  user.save()

  reset_pw.active = False
  reset_pw.save()

  return Response(status=HTTP_204_NO_CONTENT)


def __find_reset_password_attempt(token):
  try:
    return ResetPassword.objects.get(token=token, active=True)
  except ResetPassword.DoesNotExist:
    logger.error('Failed to find reset password record for token: {}'.format(token))
    raise ResetPasswordNotFoundException()


def __find_user_for_email(email):
  try:
    return User.objects.get(email=email.lower())
  except User.DoesNotExist:
    logger.error('No auth found for email: {}'.format(email, ))
    raise UserNotFoundForPasswordResetException()
