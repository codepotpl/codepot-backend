from django.db import transaction
from django.utils import timezone
from django_payu.core import (
    Buyer,
    Product as PayUProduct,
    DjangoPayU)
from django_payu.models import PayuPayment
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
    Product,
)
from codepot.views import parser_class_for_schema
from codepot.views.purchases import purchases_json_schema
from codepot.views.purchases.exceptions import (
    PromoCodeForPurchaseNotFoundException,
    PromoCodeForPurchaseNotActiveException,
    PromoCodeForPurchaseHasExceededUsageLimit,
    UserAlreadyHasPurchaseException,
    ProductNotFoundException,
    ProductInactiveException,
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
    product_id = payload['productId']
    purchase_type = payload['purchaseType']

    product = _find_and_validate_product(product_id)

    _increment_tickets_purchased(product.price_tier)

    purchase = Purchase()
    purchase.user = user
    purchase.type = purchase_type
    purchase.product = product
    purchase.save()
    discount = None

    if code:
        promo_code = _find_and_validate_promo_code(code)

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
        _set_invoice_data(purchase, invoice)

    (price_net, price_total) = _calculate_price(user, product, discount)

    if purchase_type == PurchaseTypeName.PAYU.value:
        _handle_payu_payment(user, request.META['REMOTE_ADDR'], price_total, purchase)
    elif purchase_type == PurchaseTypeName.TRANSFER.value:
        purchase.notes = 'To pay net: {}, total: {}'.format(price_net, price_total)
        purchase.payu_payment = None

    purchase.save()

    return _prepare_response(purchase)

def _check_if_user_has_purchase(user):
    try:
        p = Purchase.objects.get(user=user)
        logger.error('User: {} already has purchase: {}'.format(user.id, p.id))
        raise UserAlreadyHasPurchaseException(user.id, p.id)
    except Purchase.DoesNotExist:
        pass


def _find_and_validate_product(product_id):
    product = _find_product_or_raise(product_id)
    _check_if_product_is_active(product)
    return product

def _find_product_or_raise(product_id):
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist as e:
        logger.error('Product for ID: {} not found, err: {}'.format(product_id, e))
        raise ProductNotFoundException(product_id)

def _check_if_product_is_active(product):
    price_tier = product.price_tier
    now = timezone.now()
    date_from = price_tier.date_from
    date_to = price_tier.date_to
    if not (date_from < now < date_to):
        logger.error('Product for ID: {} is not active, from: {}, to: {}'.format(product.id, date_from, date_to))
        raise ProductInactiveException(product.id)


def _increment_tickets_purchased(price_tier):
    price_tier.tickets_purchased += 1
    price_tier.save()


def _find_and_validate_promo_code(code):
    promo_code = _find_promo_code_or_raise(code)
    _check_if_promo_code_is_active(promo_code)
    _check_if_promo_code_has_valid_usage_limit(promo_code)
    return promo_code

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


def _set_invoice_data(purchase, invoice):
    purchase.invoice_name = invoice['name']
    purchase.invoice_street = invoice['street']
    purchase.invoice_zip_code = invoice['zipCode']
    purchase.invoice_country = invoice['country']
    purchase.invoice_tax_id = invoice['taxId']

def _calculate_price(user, product, discount):
    price_net = product.price_net
    if discount:
        price_net = int(price_net - (price_net * discount) / 100)
        logger.info('New price for user: {} is: {}'.format(user.id, price_net))
    price_vat_value = product.price_vat
    price_total = int(price_net + price_net * price_vat_value)

    logger.info('User: {}, price net: {}, price total: {}'.format(user.id, price_net, price_total))

    return (price_net, price_total)


def _handle_payu_payment(user, ip_address, price_total, purchase):
    buyer = Buyer(user.first_name, user.last_name, user.email, ip_address)
    payu_product = PayUProduct(purchase.product.name, price_total, 1)
    promo_code = purchase.promo_code and purchase.promo_code.code or ''
    payment_id, follow = DjangoPayU.create_payu_payment(
        buyer, payu_product,
        'Purchase: {}, product: {}, promo code: {}'.format(purchase.id, purchase.product.id, promo_code)
    )
    purchase.payu_payment = PayuPayment.objects.get(payment_id=payment_id)
    purchase.save()


def _prepare_response(purchase):
    return Response(
        data={
            'purchaseId': purchase.id,
        },
        status=HTTP_201_CREATED
    )
