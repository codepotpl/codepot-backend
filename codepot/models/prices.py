from django.core.validators import MinValueValidator
from django.db import models


class Price(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    date_from = models.DateTimeField(unique=True, blank=False, null=False)
    date_to = models.DateTimeField(unique=True, blank=False, null=False)
    first_day = models.DecimalField(blank=False, null=False, max_digits=4, decimal_places=2,
                                    validators=[MinValueValidator(1)])
    second_day = models.DecimalField(blank=False, null=False, max_digits=4, decimal_places=2,
                                     validators=[MinValueValidator(1)])
    both_days = models.DecimalField(blank=False, null=False, max_digits=4, decimal_places=2,
                                    validators=[MinValueValidator(1)])
    tickets_purchased = models.IntegerField(default=0, blank=False, null=False)
