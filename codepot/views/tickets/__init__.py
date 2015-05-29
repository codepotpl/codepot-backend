from django.utils import timezone

from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from codepot.models import Price


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_tickets_prices(request, **kwargs):
    prices = Price.objects.all()
    now = timezone.now()

    return Response(
        data={
            'prices': [
                {
                    'name': p.name,
                    'firstDayNet': p.first_day.price_net,
                    'firstDayTotal': p.first_day.price_total,
                    'secondDayNet': p.second_day.price_net,
                    'secondDayTotal': p.second_day.price_total,
                    'bothDaysNet': p.both_days.price_net,
                    'bothDaysTotal': p.both_days.price_total,
                    'active': p.date_from < now < p.date_to,
                } for p in prices
            ],
        },
        status=HTTP_200_OK
    )
