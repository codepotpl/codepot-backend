import datetime
from enum import Enum
import string

from django.contrib.auth.models import User
from django.db import models

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


class Purchase(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=_purchase_id_value)
    user = models.OneToOneField(User)
    promo_code = models.ForeignKey('codepot.PromoCode', default=None, null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    product = models.ForeignKey('codepot.Product', null=False, blank=False)
    invoice_name = models.CharField(max_length=256, null=True, blank=True)
    invoice_street = models.CharField(max_length=256, null=True, blank=True)
    invoice_zip_code = models.CharField(max_length=256, null=True, blank=True)
    invoice_country = models.CharField(max_length=256, null=True, blank=True)
    invoice_tax_id = models.CharField(max_length=256, null=True, blank=True)
    payu_payment = models.OneToOneField('django_payu.PayuPayment', default=None, null=True, blank=True)
    payment_type = models.CharField(max_length=64, choices=enum_to_model_choices(PaymentTypeName), null=False,
                                    blank=False)
    notes = models.TextField()

    # TODO status PENDING, FINISHED, FAILED

    def __str__(self):
        return 'Purchase {} / {}'.format(self.id, self.user.id)
