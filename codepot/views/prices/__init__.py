import time

from django.utils import timezone
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from codepot.models import Product


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_prices(request, **kwargs):
    products = Product.objects.all()
    now = timezone.now()

    return Response(
        data={
            'prices': [
                {
                    'id': p.id,
                    'name': p.name,
                    'dateTo': int(time.mktime(p.price_tier.date_to.timetuple()) * 1000),
                    'priceNet': p.price_net,
                    'priceVat': p.price_vat,
                    'active': p.price_tier.date_from < now < p.price_tier.date_to,
                } for p in products
            ],
        },
        status=HTTP_200_OK
    )