from django.db import transaction
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT



@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
# @parser_classes((parser_class_for_schema(sign_up_req_schema),))
@transaction.atomic()
def handle_purchase(request, **kwargs):
    return Response(status=HTTP_204_NO_CONTENT)
