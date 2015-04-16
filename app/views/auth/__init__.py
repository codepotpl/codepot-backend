from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app import parser_class_for_schema

from app.views.auth import _schema


@api_view(['POST', ])
@permission_classes((AllowAny,))
@parser_classes((parser_class_for_schema(_schema.sign_in_req_schema),))
def sign_in(request, **kwargs):
    payload = request.DATA
    print(payload)
    return Response(status=HTTP_204_NO_CONTENT)


@api_view(['POST', ])
@permission_classes((AllowAny,))
@parser_classes((parser_class_for_schema(_schema.sign_up_req_schema),))
def sign_up(request, **kwargs):
    payload = request.DATA
    print(payload)
    return Response(status=HTTP_204_NO_CONTENT)