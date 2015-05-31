import datetime

from django.contrib.auth.models import User
from django.db import models

from codepot import create_hash


class Purchase(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=create_hash)
    user = models.OneToOneField(User)
    promo_code = models.ForeignKey('codepot.PromoCode', default=None, null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    ticket = models.OneToOneField('codepot.Ticket', null=False, blank=False)
    invoice_name = models.CharField(max_length=256, null=True, blank=True)
    invoice_street = models.CharField(max_length=256, null=True, blank=True)
    invoice_zip_code = models.CharField(max_length=256, null=True, blank=True)
    invoice_country = models.CharField(max_length=256, null=True, blank=True)
    invoice_tax_id = models.CharField(max_length=256, null=True, blank=True)
    payment = models.OneToOneField('djangopay.Payment', default=None, null=True, blank=True)
    price = models.ForeignKey('codepot.Price', null=False, blank=False)

    # TODO status
    # TODO purchase type - transfer, payu

    def __str__(self):
        return 'Purchase {} / {}'.format(self.id, self.user.id)
