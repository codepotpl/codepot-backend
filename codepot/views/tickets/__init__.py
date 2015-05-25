from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from codepot.models.tickets import TicketTypeName


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_tickets_prices(request, **kwargs):
    return Response(
        data={
            'prices': [
                {
                    'type': TicketTypeName.FIRST_DAY.value,
                    'price': 1,
                },
                {
                    'type': TicketTypeName.SECOND_DAY.value,
                    'price': 2,
                },
                {
                    'type': TicketTypeName.BOTH_DAYS.value,
                    'price': 3,
                }
            ],
        },
        status=HTTP_200_OK
    )
