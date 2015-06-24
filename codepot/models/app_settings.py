from enum import Enum

from django.db import models


class AppSettingName(Enum):
    CDPT_REGISTRATION_OPEN = 'CDPT_REGISTRATION_OPEN'


class AppSettingsManager(models.Manager):
    def is_registration_open(self):
        return self.get(name=AppSettingName.CDPT_REGISTRATION_OPEN.value).value


class AppSettings(models.Model):
    objects = AppSettingsManager()

    class Meta:
        verbose_name = 'App Settings'
        verbose_name_plural = 'App Settings'

    name = models.CharField(max_length=128, unique=True)
    value = models.BooleanField(default=True)
