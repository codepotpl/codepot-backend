from django.db import models

from codepot import create_hash


def _promo_code_value():
    return create_hash(6)


class PromoCode(models.Model):
    promo_code_id = models.CharField(primary_key=True, max_length=6, default=_promo_code_value)

    def __str__(self):
        return 'Promo code {}'.format(self.promo_code_id)
