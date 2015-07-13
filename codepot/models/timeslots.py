from enum import Enum

from django.db import models

from codepot import enum_to_model_choices, primary_key


class TimeSlotTierDayName(Enum):
    FIRST = 'FIRST'
    SECOND = 'SECOND'


class TimeSlotTier(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=primary_key)
    date_from = models.DateTimeField(blank=False)
    date_to = models.DateTimeField(blank=False)
    day = models.CharField(max_length=16, choices=enum_to_model_choices(TimeSlotTierDayName), blank=False)

    class Meta:
        unique_together = ('date_to', 'date_from', 'day')

    def __str__(self):
        return '{} / {}-{}'.format(self.day, self.date_from, self.date_to)
