from django.db import transaction
from django.utils import timezone
from djangopay.models import Product
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from codepot.logging import logger
from codepot.models import (
    PromoCode,
    Purchase,
    Price,
)
from codepot.models.tickets import Ticket
from codepot.views import parser_class_for_schema
from codepot.views.purchases import purchases_json_schema
from codepot.views.purchases.exceptions import (
    PromoCodeForPurchaseNotFoundException,
    PromoCodeForPurchaseNotActiveException,
    PromoCodeForPurchaseHasExceededUsageLimit,
    UserAlreadyHasPurchaseException,
)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
@parser_classes((parser_class_for_schema(purchases_json_schema.make_purchase_req_schema),))
@transaction.atomic()
def handle_new_purchase(request, **kwargs):
    user = request.user

    _check_if_user_has_purchase(user)

    payload = request.DATA

    code = payload['promoCode']
    invoice = payload['invoice']
    ticket_type = payload['ticketType']

    purchase = Purchase()
    purchase.user = user
    purchase.ticket = Ticket.objects.create(type=ticket_type)

    if code:
        promo_code = _find_promo_code_or_raise(code=code)
        _check_if_promo_code_is_active(promo_code)
        _check_if_promo_code_has_valid_usage_limit(promo_code)

        purchase.promo_code = promo_code
        # TODO discount 100%

        promo_code.usage_limit -= 1
        promo_code.save()

    if invoice:
        # TODO validation
        purchase.invoice_name = invoice.name
        purchase.invoice_street = invoice.street
        purchase.invoice_zip = invoice.zipCode
        purchase.invoice_country = invoice.country
        purchase.invoice_tax_id = invoice.tax_id

    current_price_tier = _get_current_price_tier()
    purchase.price = current_price_tier
    product = _get_product(current_price_tier, ticket_type)

    # TODO create payment here

    purchase.save()

    return Response(
        data={
            'purchaseId': purchase.id,
        },
        status=HTTP_201_CREATED
    )


def _check_if_user_has_purchase(user):
    try:
        p = Purchase.objects.get(user=user)
        logger.error('User: {} already has purchase: {}'.format(user.id, p.id))
        raise UserAlreadyHasPurchaseException(user.id, p.id)
    except Purchase.DoesNotExist:
        pass


def _find_promo_code_or_raise(code):
    try:
        return PromoCode.objects.get(code=code)
    except PromoCode.DoesNotExist as e:
        logger.error('Promo code for code: {} not found, err: {}'.format(code, e))
        raise PromoCodeForPurchaseNotFoundException(code)


def _check_if_promo_code_is_active(promo_code):
    if not promo_code.active:
        logger.error('Promo code: {} is not active'.format(promo_code.code))
        raise PromoCodeForPurchaseNotActiveException(promo_code.code)


def _check_if_promo_code_has_valid_usage_limit(promo_code):
    if not promo_code.usage_limit > 0:
        logger.error('Promo code: {} has exceeded usage limit'.format(promo_code.code))
        raise PromoCodeForPurchaseHasExceededUsageLimit(promo_code.code)


def _get_current_price_tier():
    now = timezone.now()
    return Price.objects.get(date_from__lt=now, date_to__gt=now)


def _get_product(current_price_tier, ticket_type):
    return Product.objects.get(name='{} {}'.format(current_price_tier.name, ticket_type.replace('_', ' ')))
