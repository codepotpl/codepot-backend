from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['POST', ])
@permission_classes((AllowAny,))
def sign_in(request, **kwargs):
    return Response(status=HTTP_204_NO_CONTENT)


@api_view(['POST', ])
@permission_classes((AllowAny,))
def sign_up(request, **kwargs):
    return Response(status=HTTP_204_NO_CONTENT)