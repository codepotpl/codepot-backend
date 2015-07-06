from django.db import models

from codepot import create_hash


class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=create_hash)
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    price_tier = models.ForeignKey('codepot.PriceTier', blank=False)
    price_net = models.IntegerField(blank=False)
    price_vat = models.FloatField(default=.23)

    def __str__(self):
        return '{}/{}'.format(self.name, self.id)
