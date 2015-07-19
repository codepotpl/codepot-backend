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
from django.conf import settings

from codepot.exceptions import (
    RegistrationClosedException,
    TicketsLimitExceededException,
)
from django_payu.core import (
    Buyer,
    Product as PayUProduct,
    DjangoPayU,
)
from django_payu.models import PayuPayment
from codepot.logging import logger
from codepot.models import (
    PromoCode,
    Purchase,
    PurchaseInvoice,
    PaymentTypeName,
    PaymentStatusName,
    Product,
    AppSettings,
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
    InvalidPaymentInfoException,
)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
@parser_classes((parser_class_for_schema(purchases_json_schema.make_purchase_req_schema),))
@transaction.atomic()
def handle_new_purchase(request, **kwargs):
    _check_if_registration_open()
    _check_if_tickets_limit_exceeded()

    user = request.user

    _check_if_user_has_purchase(user)

    payload = request.DATA

    logger.info('Handling new purchase for user: {} and payload: {}'.format(user.id, payload))

    code = payload['promoCode']
    invoice = payload['invoice']
    product_id = payload['productId']
    payment_type = payload['paymentType']
    payment_req_info = payload['paymentInfo']

    product = _find_and_validate_product(product_id)

    _validate_payment_info(payment_type, payment_req_info)

    _increment_tickets_purchased(product.price_tier)

    purchase = Purchase()
    purchase.user = user
    purchase.payment_type = payment_type
    purchase.product = product
    purchase.payment_status = PaymentStatusName.PENDING.value
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
            logger.info('Found 100% discount for user: {} and promo code: {}'.format(user.id, code))
            purchase.payment_type = PaymentTypeName.FREE.value
            purchase.payment_status = PaymentStatusName.SUCCESS.value
            purchase.save()
            return Response(build_purchase_response(purchase), HTTP_201_CREATED)

    if invoice:
        _set_invoice_data(purchase, invoice)

    (price_net, price_total) = _calculate_price(user, product, discount)
    purchase.price_net = price_net
    purchase.price_total = price_total

    if payment_type == PaymentTypeName.PAYU.value:
        redirect_link = payment_req_info['redirectLink']
        _handle_payu_payment(user, request.META['REMOTE_ADDR'], price_total, purchase, redirect_link)
    elif payment_type == PaymentTypeName.TRANSFER.value:
        purchase.notes = 'To pay net: {}, total: {}'.format(price_net, price_total)
        purchase.payu_payment = None

    purchase.save()

    return Response(build_purchase_response(purchase), HTTP_201_CREATED)


def _check_if_registration_open():
    if not AppSettings.objects.is_registration_open():
        raise RegistrationClosedException()


def _check_if_tickets_limit_exceeded():
    all_purchases = _count_success_purchases()
    organizers_purchases = _count_organizers_purchases()
    volunteers_purchases = _count_volunteers_purchases()
    speakers_purchases = _count_speakers_purchases()
    sponsors_staff_purchases = _count_sponsors_staff_purchases()
    sum_excluded = sum([organizers_purchases, volunteers_purchases, speakers_purchases, sponsors_staff_purchases, ])

    logger.info(
        'Success purchases: {}, sum excluded: {}, free: {}'.format(all_purchases, sum_excluded,
                                                                   all_purchases - sum_excluded)
    )

    if (all_purchases - sum_excluded) >= settings.MAX_TICKETS:
        raise TicketsLimitExceededException()


def _count_success_purchases():
    return Purchase.objects.filter(payment_status=PaymentStatusName.SUCCESS.value).count()


def _count_organizers_purchases():
    return __count_purchases_for_promo_code_classification('organizers')


def _count_volunteers_purchases():
    return __count_purchases_for_promo_code_classification('volunteers')


def _count_speakers_purchases():
    return __count_purchases_for_promo_code_classification('speakers')


def _count_sponsors_staff_purchases():
    return __count_purchases_for_promo_code_classification('sponsors staff')


def __count_purchases_for_promo_code_classification(classification):
    return Purchase.objects.filter(promo_code__classification__name__istartswith=classification).count()

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


def _validate_payment_info(payment_type, payment_info):
    if payment_type == PaymentTypeName.PAYU.value:
        if not payment_info or not payment_info.get('redirectLink', None):
            raise InvalidPaymentInfoException("'redirectLink' is required for PAYU payment type.")

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
    purchase_invoice = PurchaseInvoice()
    purchase_invoice.name = invoice['name']
    purchase_invoice.street = invoice['street']
    purchase_invoice.zip_code = invoice['zipCode']
    purchase_invoice.city = invoice['city']
    purchase_invoice.country = invoice['country']
    purchase_invoice.tax_id = invoice['taxId']
    purchase_invoice.purchase = purchase
    purchase_invoice.save()

def _calculate_price(user, product, discount):
    price_net = product.price_net
    if discount:
        price_net = int(price_net - (price_net * discount) / 100)
        logger.info('New price for user: {} is: {}'.format(user.id, price_net))
    price_vat_value = product.price_vat
    price_total = int(price_net + price_net * price_vat_value)

    logger.info('User: {}, price net: {}, price total: {}'.format(user.id, price_net, price_total))

    return (price_net, price_total)


def _handle_payu_payment(user, ip_address, price_total, purchase, redirect_link):
    buyer = Buyer(user.first_name, user.last_name, user.email, ip_address)
    payu_product = PayUProduct(purchase.product.name, price_total, 1)
    promo_code = purchase.promo_code and purchase.promo_code.code or ''
    payment_id, follow = DjangoPayU.create_payu_payment(
        buyer,
        payu_product,
        'Purchase: {}, product: {}, promo code: {}'.format(purchase.id, purchase.product.id, promo_code),
        redirect_link
    )
    purchase.payu_payment = PayuPayment.objects.get(payment_id=payment_id)
    purchase.payu_payment_link = follow


def build_purchase_response(purchase):
    return {
        'purchase': {
        'id': purchase.id,
        'promoCode': purchase.promo_code and purchase.promo_code.code or None,
        'created': purchase.created,
        'product': purchase.product.id,
        'invoice': _get_purchase_invoice_data_or_none(purchase),
        'paymentType': purchase.payment_type,
        'paymentStatus': purchase.payment_status,
        'paymentInfo': _prepare_payment_info(purchase),
        'priceNet': purchase.price_net,
        'priceTotal': purchase.price_total,
        }
    }


def _get_purchase_invoice_data_or_none(purchase):
    try:
        invoice = PurchaseInvoice.objects.get(purchase=purchase)
        return {
            'name': invoice.name,
            'street': invoice.street,
            'city': invoice.city,
            'zipCode': invoice.zip_code,
            'country': invoice.country,
            'taxId': invoice.tax_id,
        }
    except PurchaseInvoice.DoesNotExist as e:
        logger.info('Skipping invoice processing, no invoice for purchase: {}, err: {}'.format(purchase.id, str(e)))
        return None


def _prepare_payment_info(purchase):
    if purchase.payment_type == PaymentTypeName.FREE.value:
        return None
    elif purchase.payment_type == PaymentTypeName.PAYU.value:
        return {
            'paymentLink': purchase.payu_payment_link,
        }
    elif purchase.payment_type == PaymentTypeName.TRANSFER.value:
        return _prepare_transfer_payment_info(purchase)
    else:
        raise Exception(
            'Invalid purchase payment type. Purchase: {}, payment type: {}'.format(purchase.id, purchase.payment_type))


def _prepare_transfer_payment_info(purchase):
    ret = {}
    ret.update({
        'title': 'Codepot: {}'.format(purchase.id)
    })
    ret.update(settings.MCE_BANK_ACCOUNT)
    return {'transferData': ret}
