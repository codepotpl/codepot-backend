from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.compat import EmailValidator
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from codepot.logging import logger
from codepot.utils import get_rendered_template
from codepot.views import (
    parser_class_for_schema,
    validate_payload_with_schema,
)
from ._util import prepare_auth_response_map
from .auth_json_schema import sign_up_req_schema
from codepot.views.auth.exceptions import (
    InvalidEmailAddressException,
    EmailAddressAlreadyUsedException,
)
from celerytq.tasks import send_mail


@api_view(['POST', ])
@permission_classes((AllowAny,))
@parser_classes((parser_class_for_schema(sign_up_req_schema),))
@transaction.atomic()
def sign_up(request, **kwargs):
    payload = request.DATA

    validate_payload_with_schema(payload, sign_up_req_schema)

    email = payload['email']
    password = payload['password']
    first_name = payload['firstName']
    last_name = payload['lastName']

    _validate_email(email)

    user = _create_user(email, password, first_name, last_name)

    _send_registration_email(email, '{} {}'.format(first_name, last_name))

    response_map = prepare_auth_response_map(user)

    return Response(
        status=HTTP_201_CREATED,
        headers=response_map['headers'],
        data=response_map['data']
    )


def _validate_email(email):
    try:
        validator = EmailValidator()
        validator(email)
    except ValidationError as e:
        raise InvalidEmailAddressException()


def _create_user(email, password, first_name, last_name):
    try:
        user = User.objects.create_user(email, email, password, first_name=first_name, last_name=last_name)

        _get_or_generate_token(user)

        return user

    except IntegrityError as e:
        raise EmailAddressAlreadyUsedException()


def _get_or_generate_token(user):
    try:
        return Token.objects.get(user=user)
    except Token.DoesNotExist:
        logger.info('No token found for user: %s. New token will be generated.'.format(user.id))
        return Token.objects.create(user=user)


def _send_registration_email(email, name):
    send_mail.delay(email, 'Welcome {}!'.format(name),
                    get_rendered_template('mail/registration_confirmation.txt', {'name': name}),
                    get_rendered_template('mail/registration_confirmation.html', {'name': name}),
                    ['tickets@codepot.pl'])
