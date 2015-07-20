import datetime
from enum import Enum
import string

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.db import transaction

from codepot import (
    create_hash,
    enum_to_model_choices,
)


def _purchase_id_value():
    return create_hash(16, string.ascii_uppercase + string.digits)


class PaymentTypeName(Enum):
    PAYU = 'PAYU'
    TRANSFER = 'TRANSFER'
    FREE = 'FREE'
    GROUP = 'GROUP'


class PaymentStatusName(Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    STARTED = 'STARTED'  # PayU dedicated only


class Purchase(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=_purchase_id_value)
    user = models.OneToOneField(User)
    promo_code = models.ForeignKey('codepot.PromoCode', default=None, null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now, blank=False)
    product = models.ForeignKey('codepot.Product', blank=False)
    payu_payment = models.OneToOneField('django_payu.PayuPayment', default=None, null=True, blank=True)
    payment_type = models.CharField(max_length=64, choices=enum_to_model_choices(PaymentTypeName), blank=False)
    payment_status = models.CharField(max_length=32, choices=enum_to_model_choices(PaymentStatusName), blank=False,
                                      default=PaymentStatusName.PENDING.value)
    price_net = models.IntegerField(blank=False, default=0)
    price_total = models.IntegerField(blank=False, default=0)
    payu_payment_link = models.URLField(max_length=4096, null=True, blank=True, default=None)
    notes = models.TextField(blank=True, null=True)
    fake = models.BooleanField(default=False)
    confirmation_sent = models.BooleanField(default=False)

    def __str__(self):
        return '{}/{}'.format(self.id, self.user.id)


@receiver(post_delete, sender=Purchase)
def decrement_tickets_sold_counter_on_purchase_deletion(sender, instance, **kwargs):
    with transaction.atomic():
        price_tier = instance.product.price_tier
        price_tier.tickets_purchased -= 1
        price_tier.save()


class PurchaseInvoice(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=_purchase_id_value)
    purchase = models.OneToOneField('codepot.Purchase', blank=True, null=True)
    no = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, blank=False)
    street = models.CharField(max_length=256, blank=False)
    city = models.CharField(max_length=256, blank=False)
    zip_code = models.CharField(max_length=256, blank=False)
    country = models.CharField(max_length=256, blank=False)
    tax_id = models.CharField(max_length=256, blank=False)
    ifirma_id = models.CharField(max_length=256, blank=True, null=True)
    sent = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return '{}/{}'.format(self.id, self.purchase.id)
