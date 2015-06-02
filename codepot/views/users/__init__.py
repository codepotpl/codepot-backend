from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from codepot.logging import logger
from codepot.models import Purchase
from codepot.views.auth.exceptions import InvalidUserIdException
from codepot.views.purchases.exceptions import UserPurchaseNotFoundException


def _compare_ids_and_raise_exception_if_different(endpoint_id, user_id):
    if str(endpoint_id) != str(user_id):
        logger.error('Id does not match: %s and: %s' % (endpoint_id, user_id))
        raise InvalidUserIdException()


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_user_purchase(request, **kwargs):
    user = request.user
    user_id = kwargs['user_id']
    _compare_ids_and_raise_exception_if_different(user_id, user.id)
    purchase = _find_purchase_for_user_or_raise(user)

    return Response(
        status=HTTP_200_OK,
        data={
            'purchase': {
                'purchaseId': purchase.id,
                'promoCode': purchase.promo_code and purchase.promo_code.code or None,
                'created': purchase.created,
                'product': purchase.product.id,
                'invoice': {
                    'name': purchase.invoice_name,
                    'street': purchase.invoice_street,
                    'zipCode': purchase.invoice_zip_code,
                    'country': purchase.invoice_country,
                    'taxId': purchase.invoice_tax_id,
                } if not _all_invoice_fields_empty(purchase) else None,
                'paymentType': purchase.payment_type,
                'paymentStatus': purchase.payment_status,
            },
        }
    )


def _find_purchase_for_user_or_raise(user):
    try:
        return Purchase.objects.get(user=user)
    except Purchase.DoesNotExist as e:
        logger.error('No purchase found for user with ID: {}, err: {}'.format(user.id, str(e)))
        raise UserPurchaseNotFoundException(user.id)


def _all_invoice_fields_empty(purchase):
    invoice_keys = list(filter(lambda x: x.startswith('invoice_'), purchase.__dict__.keys()))
    invoice_values = [getattr(purchase, k) for k in invoice_keys]
    return not bool(list(filter(lambda x: bool(x), invoice_values)))
