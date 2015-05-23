from django.contrib.auth.models import User

from django.db import models

from codepot import create_hash


class Purchase(models.Model):
    purchase_id = models.CharField(primary_key=True, max_length=32, default=create_hash)
    user = models.OneToOneField(User)
    promo_code = models.ForeignKey('codepot.PromoCode', default=None, null=True, blank=True)

    def __str__(self):
        return 'Purchase {} / {}'.format(self.purchase_id, self.user.id)
