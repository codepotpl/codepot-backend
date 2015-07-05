import datetime
import string

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models

from codepot import create_hash
from codepot.logging import logger


def _promo_code_value():
    return create_hash(6, char_set=string.ascii_uppercase + string.digits)


class PromoCodeClassification(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class PromoCode(models.Model):
    code = models.CharField(primary_key=True, max_length=6, default=_promo_code_value)
    usage_limit = models.IntegerField(default=1, validators=[MinValueValidator(0)], null=False, blank=False)
    active = models.BooleanField(default=True)
    discount = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                           null=False,
                                           blank=False)
    sent = models.BooleanField(default=False)
    contact_info = models.TextField(default=None, null=True, blank=True)
    notes = models.TextField(default=None, null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    valid_from = models.DateField(default=None, blank=True, null=True)
    valid_to = models.DateField(default=None, blank=True, null=True)
    classification = models.ForeignKey('codepot.PromoCodeClassification', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.usage_limit == 0:
            self.active = False
            logger.info('Setting promo code: {} to inactive.'.format(self.code))
        super(PromoCode, self).save(*args, **kwargs)

    def __str__(self):
        return self.code
