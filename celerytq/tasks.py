from django.core.mail import EmailMultiAlternatives

from getenv import env
from celery import shared_task
from django.db import transaction
from haystack.management.commands import update_index

from python_ifirma.core import (
    iFirmaAPI,
    Client as iFirmaClient,
    Address as iFirmaAddress,
    Position as iFirmaItem,
    NewInvoiceParams as iFirmaInvoiceParams,
    VAT,
)
from django_payu.helpers import PaymentStatus as PayUPaymentStatus
from codepot.logging import logger
from codepot.models import (
    Purchase,
    PurchaseInvoice,
    PaymentStatusName,
)
from codepot.models.purchases import PaymentTypeName
from codepot.utils import get_rendered_template

_ifirma_client = iFirmaAPI(env('CDPT_IFIRMA_USER'), env('CDPT_IFIRMA_INVOICE_KEY'), env('CDPT_IFIRMA_USER_KEY'))


@shared_task
def check_payu_payment_status():
  logger.info('Checking payment status.')
  with transaction.atomic():

    pending_purchases = Purchase.objects.filter(
      payment_status__in=[PaymentStatusName.PENDING.value, PaymentStatusName.STARTED.value],
      payment_type=PaymentTypeName.PAYU.value
    )
    logger.info('Found: {} pending payments.'.format(pending_purchases.count()))

    for purchase in pending_purchases:

      purchase_id = purchase.id
      logger.info('Checking payment status for purchase: {}, current payment status: {}'.format(
        purchase_id, purchase.payment_status
      ))
      payu_payment = purchase.payu_payment
      payu_payment_status = payu_payment.payment_status

      logger.info('Current PayU status: {}, purchase: {}'.format(payu_payment_status, purchase_id))

      if payu_payment_status.lower() == PayUPaymentStatus.STATUS_COMPLETED:
        purchase.payment_status = PaymentStatusName.SUCCESS.value
      elif payu_payment_status.lower() == PayUPaymentStatus.STATUS_FAILED:
        purchase.payment_status = PaymentStatusName.FAILED.value
      elif payu_payment_status.lower() == PayUPaymentStatus.STATUS_STARTED:
        purchase.payment_status = PaymentStatusName.STARTED.value

      logger.info('New purchase status: {}, purchase: {}'.format(purchase.payment_status, purchase_id))

      purchase.save()

  return None


@shared_task
def send_payment_notification():
  logger.info('Sending payment notification')

  with transaction.atomic():
    finished_purchases = Purchase.objects.filter(
      payment_status__in=[PaymentStatusName.SUCCESS.value, PaymentStatusName.FAILED.value],
      confirmation_sent=False
    )
    logger.info('Found: {} finished payments.'.format(finished_purchases.count()))

    for purchase in finished_purchases:
      completed = purchase.payment_status == PaymentStatusName.SUCCESS.value
      subject = 'Purchase completed [{}]'.format(purchase.id) if completed else 'Purchase failed [{}]'.format(
        purchase.id)
      user = purchase.user
      template = 'completed' if completed else 'failed'

      send_mail.delay(
        user.email,
        subject,
        get_rendered_template('mail/purchase/{}.txt'.format(template),
                              {'name': user.first_name, 'purchase_id': purchase.id}),
        get_rendered_template('mail/purchase/{}.html'.format(template),
                              {'name': user.first_name, 'purchase_id': purchase.id}),
        ['tickets@codepot.pl']
      )

      purchase.confirmation_sent = True
      purchase.save()


@shared_task()
def generate_and_send_invoice():
  logger.info('Generating and sending invoices.')

  unsent_invoices = PurchaseInvoice.objects.filter(
    sent=False,
    purchase__payment_status=PaymentStatusName.SUCCESS.value,
    purchase__confirmation_sent=True
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
          float("{0:.2f}".format(purchase.price_total / 100.0)),
          u"Bilet wstępu na warsztaty codepot.pl: {}".format(purchase.id),
          "szt."
        )
        ifirma_invoice = iFirmaInvoiceParams(client, [position])
        (ifirma_invoice_id, ifirma_invoice_no) = _ifirma_client.generate_invoice(ifirma_invoice)
        ifirma_invoice_pdf = _ifirma_client.get_invoice_pdf(ifirma_invoice_id)

        invoice.ifirma_id = ifirma_invoice_id
        send_mail(
          purchase.user.email,
          'Payment completed [{}]'.format(purchase.id),
          get_rendered_template(
            'mail/purchase/invoice.txt',
            {'name': purchase.user.first_name, 'purchase_id': purchase.id}
          ),
          get_rendered_template(
            'mail/purchase/invoice.html',
            {'name': purchase.user.first_name, 'purchase_id': purchase.id}
          ),
          ['tickets@codepot.pl'],
          ('{}.pdf'.format(ifirma_invoice_no), ifirma_invoice_pdf.getvalue(), 'application/pdf')
        )
        invoice.no = ifirma_invoice_no
        invoice.sent = True

        invoice.save()
      except Exception as e:
        logger.error('Error while generating invoice for purchase: {}, err: {}.'.format(purchase.id, str(e)))
        continue


@shared_task
def send_mail(to, title, messageTXT, messageHTML, bcc=None, attachment=[]):
  '''
  :param to:
  :param title:
  :param messageTXT:
  :param messageHTML:
  :param bcc:
  :param attachment: (filename, content, mimetype)
  :return:
  '''
  logger.info(
    'Sending email to: {}, title: {}, messageTXT: {}, messageHTML: {}, bcc: {}, attachment: {}'.format(to, title,
                                                                                                       messageTXT,
                                                                                                       messageHTML, bcc,
                                                                                                       bool(
                                                                                                         attachment)))
  email = EmailMultiAlternatives(
    subject=title,
    body=messageTXT,
    from_email='donotreply@codepot.pl',
    to=[to],
    bcc=bcc,
    attachments=attachment and [attachment] or []
  )
  email.attach_alternative(messageHTML, "text/html")
  email.send()


@shared_task
def update_workshops_full_text_search():
  logger.info('Updating workshop full-text search index.')
  try:
    update_index.Command().handle(using=['default'], verbosity=2, remove=True)
  except Exception as e:
    logger.error('Caught exception while updating workshop index: %s' % e)

  return None
