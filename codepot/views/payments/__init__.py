from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from codepot.logging import logger


@api_view(['GET', ])
@transaction.atomic()
def handle_payment(request, **kwargs):
    logger.info(request.DATA)
    logger.info(request.GET['payment_id'])

    return Response(data={}, status=HTTP_200_OK)

    # TODO payment_status = DjangoPayU.get_payment_status(payment_id)
