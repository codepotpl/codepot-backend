from django.db import transaction
from django.utils import timezone
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
    PurchaseTypeName,
    Price,
    Ticket,
)
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

    logger.info('Handling new purchase for user: {} and payload: {}'.format(user.id, payload))

    code = payload['promoCode']
    invoice = payload['invoice']
    ticket_type = payload['ticketType']
    purchase_type = payload['purchaseType']

    purchase = Purchase()
    purchase.user = user
    purchase.type = purchase_type
    purchase.ticket = Ticket.objects.create(type=ticket_type)
    discount = None

    current_price_tier = _get_current_price_tier()
    current_price_tier.tickets_purchased += 1
    current_price_tier.save()
    purchase.price = current_price_tier

    if code:
        promo_code = _find_promo_code_or_raise(code=code)
        _check_if_promo_code_is_active(promo_code)
        _check_if_promo_code_has_valid_usage_limit(promo_code)

        purchase.promo_code = promo_code
        promo_code.usage_limit -= 1
        promo_code.save()
        discount = promo_code.discount

        logger.info('Found promo code: {} for user: {}, discount: {}'.format(code, user.id, discount))

        if discount == 100:
            purchase.type = PurchaseTypeName.FREE.value
            logger.info('Found 100% discount for user: {} and promo code: {}'.format(user.id, code))
            purchase.save()
            return _prepare_response(purchase)

    if invoice:
        purchase.invoice_name = invoice['name']
        purchase.invoice_street = invoice['street']
        purchase.invoice_zip_code = invoice['zipCode']
        purchase.invoice_country = invoice['country']
        purchase.invoice_tax_id = invoice['taxId']

    (price_net, price_total) = _calculate_price(user, current_price_tier, ticket_type, discount)

    if purchase_type == PurchaseTypeName.PAYU.value:
        # TODO create payment here
        pass
    elif purchase_type == PurchaseTypeName.TRANSFER.value:
        # TODO what should be done here
        purchase.payment == None

    purchase.save()

    return _prepare_response(purchase)

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

def _prepare_response(purchase):
    return Response(
        data={
            'purchaseId': purchase.id,
        },
        status=HTTP_201_CREATED
    )

def _calculate_price(user, current_price_tier, ticket_type, discount):
    price_net = getattr(current_price_tier, '{}_net'.format(ticket_type.lower()))
    if discount:
        price_net = int(price_net - (price_net * discount) / 100)
        logger.info('New price for user: {} is: {}'.format(user.id, price_net))
    price_vat_value = getattr(current_price_tier, '{}_vat'.format(ticket_type.lower()))
    price_total = int(price_net + price_net * price_vat_value)

    logger.info('User: {}, price net: {}, price total: {}'.format(user.id, price_net, price_total))

    return (price_net, price_total)
