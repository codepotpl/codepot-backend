from django.db import transaction
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django_payu.helpers import PaymentStatus as PayUPaymentStatus

from codepot.logging import logger
from codepot.models import (
    Purchase,
    PaymentStatusName,
    PaymentTypeName,
)
from codepot.views.auth.exceptions import InvalidUserIdException
from codepot.views.purchases.exceptions import UserPurchaseNotFoundException
from codepot.views.purchases import build_purchase_response


def _compare_ids_and_raise_exception_if_different(endpoint_id, user_id):
    if str(endpoint_id) != str(user_id):
        logger.error('Id does not match: %s and: %s' % (endpoint_id, user_id))
        raise InvalidUserIdException()


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
@transaction.atomic()
# TODO invoice generation
def get_user_purchase(request, **kwargs):
    user = request.user
    user_id = kwargs['user_id']
    _compare_ids_and_raise_exception_if_different(user_id, user.id)

    purchase = _find_purchase_for_user_or_raise(user)

    _handle_purchase_payment_status(purchase)
    _generate_invoice_if_needed(purchase)

    return Response(
        status=HTTP_200_OK,
        data=build_purchase_response(purchase)
    )


def _find_purchase_for_user_or_raise(user):
    try:
        return Purchase.objects.get(user=user)
    except Purchase.DoesNotExist as e:
        logger.error('No purchase found for user with ID: {}, err: {}'.format(user.id, str(e)))
        raise UserPurchaseNotFoundException(user.id)


def _handle_purchase_payment_status(purchase):
    if purchase.payment_status == PaymentStatusName.PENDING.value and purchase.payment_type == PaymentTypeName.PAYU.value:
        payu_payment = purchase.payu_payment
        payu_payment_status = payu_payment.payment_status
        if payu_payment_status.lower() == PayUPaymentStatus.STATUS_COMPLETED:
            payu_payment.payment_status = PaymentStatusName.SUCCESS.value
            purchase.save()
        elif payu_payment_status.lower() == PayUPaymentStatus.STATUS_FAILED:
            payu_payment.payment_status = PaymentStatusName.FAILED.value
            purchase.save()


def _generate_invoice_if_needed(purchase):
    pass
