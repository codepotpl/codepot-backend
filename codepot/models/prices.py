from django.db import models


class PriceTier(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    date_from = models.DateTimeField(unique=True, blank=False, null=False)
    date_to = models.DateTimeField(unique=True, blank=False, null=False)
    tickets_purchased = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

