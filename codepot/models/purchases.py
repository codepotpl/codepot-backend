import datetime

from django.contrib.auth.models import User
from django.db import models

from codepot import create_hash


class Purchase(models.Model):
    purchase_id = models.CharField(primary_key=True, max_length=32, default=create_hash)
    user = models.OneToOneField(User)
    promo_code = models.ForeignKey('codepot.PromoCode', default=None, null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    ticket = models.OneToOneField('codepot.Ticket', null=False, blank=False)
    invoice_name = models.CharField(max_length=256, null=True, blank=True)
    invoice_street = models.CharField(max_length=256, null=True, blank=True)
    invoice_zip = models.CharField(max_length=256, null=True, blank=True)
    invoice_country = models.CharField(max_length=256, null=True, blank=True)
    invoice_tax_id = models.CharField(max_length=256, null=True, blank=True)
    payment = models.OneToOneField('djangopay.Payment', default=None, null=True, blank=True)

    # TODO status
    # TODO purchase type - transfer, payu

    def __str__(self):
        return 'Purchase {} / {}'.format(self.purchase_id, self.user.id)
