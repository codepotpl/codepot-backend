from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from app.logging import logger
from app.views import (
    parser_class_for_schema,
    validate_payload_with_schema,
)
from app.views.auth.exceptions import LoginFailedException
from .auth_json_schema import sign_in_req_schema
from ._util import prepare_auth_response_map


@api_view(['POST', ])
@permission_classes((AllowAny,))
@parser_classes((parser_class_for_schema(sign_in_req_schema),))
@transaction.atomic()
def sign_in(request, **kwargs):
    payload = request.DATA

    validate_payload_with_schema(payload, sign_in_req_schema)

    email = payload['email']
    password = payload['password']
    user = _find_user_for_email(email)
    _check_password(email, password, user.password)
    response_map = prepare_auth_response_map(user)

    return Response(
        status=HTTP_200_OK,
        headers=response_map['headers'],
        data=response_map['data']
    )


def _find_user_for_email(email):
    try:
        return User.objects.get(username=email)
    except User.DoesNotExist as e:
        logger.error('No user found for email: {}, err: {}.'.format(email, str(e)))
        raise LoginFailedException()


def _check_password(email, query_password, db_password):
    if not check_password(query_password, db_password):
        logger.error('Password verification failed for user with email: {}.'.format(email))
        raise LoginFailedException()
