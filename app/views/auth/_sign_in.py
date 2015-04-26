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

from app.views import parser_class_for_schema
from app.views.auth import (
    _schema,
    _prepare_auth_response_map,
)
from app.views.auth.exceptions import (
    UserNotFoundException,
    InvalidPasswordException,
)


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
    response_map = _prepare_auth_response_map(user)

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
