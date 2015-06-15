from celery import shared_task
from django.core.mail import send_mail as d_send_mail
from django.db import transaction
from django_payu.helpers import PaymentStatus as PayUPaymentStatus

from codepot.logging import logger
from codepot.models import (
    Purchase,
    PaymentStatusName,
)


@shared_task
def send_mail(to, title, message):
    logger.info('Sending email to: {}, title: {}, message: {}'.format(to, title, message))
    return d_send_mail(title, message, 'donotreply@codepot.pl', [to])


@shared_task
def check_payment_status():
    logger.info('Checking payment status.')
    with transaction.atomic():
        pending_purchases = Purchase.objects.filter(payment_status=PaymentStatusName.PENDING.value)
        for purchase in pending_purchases:
            purchase_id = purchase.id
            logger.info('Checking payment status for purchase: {}, current payment status: {}'.format(
                purchase_id, purchase.payment_status))
            payu_payment = purchase.payu_payment
            payu_payment_status = payu_payment.payment_status

            logger.info('Current PayU status: {}, purchase: {}'.format(payu_payment_status, purchase_id))

            if payu_payment_status.lower() == PayUPaymentStatus.STATUS_COMPLETED:
                purchase.payment_status = PaymentStatusName.SUCCESS.value
            elif payu_payment_status.lower() == PayUPaymentStatus.STATUS_FAILED:
                purchase.payment_status = PaymentStatusName.FAILED.value

            logger.info('New purchase status: {}, purchase: {}'.format(purchase.payment_status, purchase_id))

            purchase.save()

    return None

@shared_task
def add(x, y):
    return x + y