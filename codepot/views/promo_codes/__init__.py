from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from codepot.logging import logger
from codepot.models.promo_codes import PromoCode
from codepot.views.promo_codes.exceptions import PromoCodeNotFoundException


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_promo_code_for_id(request, **kwargs):
    promo_code_id = kwargs['promo_code_id']
    promo_code = _find_promo_code_for_id_or_raise(promo_code_id)
    return Response(
        status=HTTP_200_OK,
        data={
            'promoCodeId': promo_code.code,
            'active': promo_code.active,
            'discount': promo_code.discount,
        }
    )


def _find_promo_code_for_id_or_raise(promo_code_id):
    try:
        return PromoCode.objects.get(code=promo_code_id)
    except PromoCode.DoesNotExist as e:
        logger.error('Promo code for ID: {} not found, err: {}'.format(promo_code_id, str(e)))
        raise PromoCodeNotFoundException(promo_code_id)
