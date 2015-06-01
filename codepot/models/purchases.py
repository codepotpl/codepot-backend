import datetime
from enum import Enum

from django.contrib.auth.models import User
from django.db import models

from codepot import (
    create_hash,
    enum_to_model_choices,
)


class PurchaseTypeName(Enum):
    PAYU = 'PAYU'
    TRANSFER = 'TRANSFER'
    FREE = 'FREE'


class Purchase(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=create_hash)
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
    type = models.CharField(max_length=64, choices=enum_to_model_choices(PurchaseTypeName), null=False, blank=False)
    notes = models.TextField()

    # TODO status PENDING, FINISHED, FAILED

    def __str__(self):
        return 'Purchase {} / {}'.format(self.id, self.user.id)
