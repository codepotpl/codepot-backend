from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    price_tier = models.ForeignKey('codepot.PriceTier', blank=False)
    price_net = models.IntegerField(blank=False)
    price_total = models.IntegerField(blank=False)
