from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import (
    transaction,
    IntegrityError,
)
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
)
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.logging import logger
from app.models import UserProfile
from app.views import parser_class_for_schema
from app.views.auth import _schema
from app.views.auth.exceptions import (
    EmailAddressAlreadyUsedException,
    InvalidEmailAddressException,
    UserNotFoundException,
    InvalidPasswordException,
)


def validate_email(email):
    try:
        validator = EmailValidator()
        validator(email)
    except ValidationError as e:
        raise InvalidEmailAddressException()


def get_or_generate_token(user):
    try:
        return Token.objects.get(user=user)
    except Token.DoesNotExist:
        logger.info('No token found for user: %s. New token will be generated.'.format(user.id))
        return Token.objects.create(user=user)


@api_view(['POST', ])
@permission_classes((AllowAny,))
@parser_classes((parser_class_for_schema(_schema.sign_in_req_schema),))
@transaction.atomic()
def sign_in(request, **kwargs):
    payload = request.DATA
    email = payload['email']
    password = payload['password']
    user = _find_user_for_email(email)
    _check_password(password, user.password)
    response_map = _prepare_response_map(user)

    return Response(
        status=HTTP_200_OK,
        headers=response_map['headers'],
        data=response_map['data']
    )


def _find_user_for_email(email):
    try:
        return User.objects.get(username=email)
    except User.DoesNotExist as e:
        raise UserNotFoundException()


def _check_password(query_password, db_password):
    if not check_password(query_password, db_password):
        raise InvalidPasswordException()


@api_view(['POST', ])
@permission_classes((AllowAny,))
@parser_classes((parser_class_for_schema(_schema.sign_up_req_schema),))
@transaction.atomic()
def sign_up(request, **kwargs):
    payload = request.DATA

    email = payload['email']
    password = payload['password']
    first_name = payload['firstName']
    last_name = payload['lastName']

    validate_email(email)

    user = _create_user(email, password, first_name, last_name)
    response_map = _prepare_response_map(user)

    return Response(
        status=HTTP_201_CREATED,
        headers=response_map['headers'],
        data=response_map['data']
    )


def _create_user(email, password, first_name, last_name):
    try:
        user = User.objects.create_user(email, email, password)

        UserProfile.objects.create(
            user=user,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        get_or_generate_token(user)

        return user

    except IntegrityError as e:
        raise EmailAddressAlreadyUsedException()


def _prepare_response_map(user):
    return {
        'headers': {
            'Token': user.auth_token.key
        },
        'data': {
            'id': user.id,
            'email': user.userprofile.email,
            'firstName': user.userprofile.first_name,
            'lastName': user.userprofile.last_name,
        }
    }