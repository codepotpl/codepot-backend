from getenv import env
from celery import shared_task
from django.core.mail import send_mail as d_send_mail
from django.db import transaction
from django_payu.helpers import PaymentStatus as PayUPaymentStatus
from python_ifirma.core import (
    iFirmaAPI,
    Client as iFirmaClient,
    Address as iFirmaAddress,
    Position as iFirmaItem,
    NewInvoiceParams as iFirmaInvoiceParams,
    VAT, )

from codepot.logging import logger
from codepot.models import (
    Purchase,
    PaymentStatusName,
)
from codepot.models.purchases import PurchaseInvoice

_ifirma_client = iFirmaAPI('$DEMO254449', env('CDPT_IFIRMA_INVOICE_KEY'), env('CDPT_IFIRMA_USER_KEY'))

@shared_task
def send_mail(to, title, message):
    logger.info('Sending email to: {}, title: {}, message: {}'.format(to, title, message))
    return d_send_mail(title, message, 'donotreply@codepot.pl', [to])


@shared_task
def check_payment_status():
    logger.info('Checking payment status.')
    with transaction.atomic():
        pending_purchases = Purchase.objects.filter(payment_status=PaymentStatusName.PENDING.value)
        logger.info('Found: {} pending payments.'.format(pending_purchases.count()))
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
                #TODO mailing o failu

            logger.info('New purchase status: {}, purchase: {}'.format(purchase.payment_status, purchase_id))

            purchase.save()

    return None


@shared_task()
def generate_and_send_invoice():
    logger.info('Generating and sending invoices.')

    unsent_invoices = PurchaseInvoice.objects.filter(
        sent=False,
        purchase__payment_status=PaymentStatusName.SUCCESS.value
    )
    logger.info('Found: {} unsent invoices.'.format(unsent_invoices.count()))

    for invoice in unsent_invoices:
        with transaction.atomic():
            try:

                purchase = invoice.purchase
                logger.info('Generating invoice for purchase: {}'.format(purchase.id))

                client = iFirmaClient(
                    invoice.name,
                    invoice.tax_id,
                    iFirmaAddress(
                        invoice.city,
                        invoice.zip_code,
                        invoice.street,
                        invoice.country,
                    )
                )
                position = iFirmaItem(
                    VAT.VAT_23,
                    1,
                    purchase.price_net,
                    u"Bilet wstępu na warsztaty codepot.pl: {}".format(purchase.id),
                    "szt."
                )
                ifirma_invoice = iFirmaInvoiceParams(client, [position])
                invoice_id = _ifirma_client.generate_invoice(ifirma_invoice)
                # TODO PDF
                # TODO email sending

                invoice.ifirma_id = invoice_id
                invoice.sent = True
                invoice.save()

            except Exception as e:
                logger.error('Error while generating invoice for purchase: {}, err: {}.'.format(purchase.id, str(e)))

# TODO integracja z PayU
# TODO celery shutting down - screen  - supiervisord
