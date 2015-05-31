from django.db import models


class Price(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    date_from = models.DateTimeField(unique=True, blank=False, null=False)
    date_to = models.DateTimeField(unique=True, blank=False, null=False)
    tickets_purchased = models.IntegerField(default=0, blank=False, null=False)
    first_day_net = models.IntegerField()
    first_day_total = models.IntegerField()
    first_day_vat = models.FloatField(default=0.23)
    second_day_net = models.IntegerField()
    second_day_total = models.IntegerField()
    second_day_vat = models.FloatField(default=0.23)
    both_days_net = models.IntegerField()
    both_days_total = models.IntegerField()
    both_days_vat = models.FloatField(default=0.23)
