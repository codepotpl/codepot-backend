from django.db import models


class Price(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    date_from = models.DateTimeField(unique=True, blank=False, null=False)
    date_to = models.DateTimeField(unique=True, blank=False, null=False)
    tickets_purchased = models.IntegerField(default=0, blank=False, null=False)
    first_day = models.ForeignKey('djangopay.Product', unique=True, null=False, blank=False, related_name='+')
    second_day = models.ForeignKey('djangopay.Product', unique=True, null=False, blank=False, related_name='+')
    both_days = models.ForeignKey('djangopay.Product', unique=True, null=False, blank=False, related_name='+')
