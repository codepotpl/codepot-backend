from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from codepot import primary_key


class WorkshopTag(models.Model):
    name = models.CharField(primary_key=True, max_length=256, blank=False, unique=True)

    def __str__(self):
        return self.name


class Workshop(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=primary_key)
    title = models.CharField(max_length=512, blank=False)
    description = models.TextField(blank=False)
    tags = models.ManyToManyField('codepot.WorkshopTag')
    mentors = models.ManyToManyField(User, related_name='mentors')
    attendees = models.ManyToManyField(User, related_name='attendees')
    max_attendees = models.IntegerField(default=50, validators=[MinValueValidator(0)], blank=False)
    room_no = models.IntegerField(validators=[MinValueValidator(0)])
    timeslots = models.ManyToManyField('codepot.TimeSlotTier')

    def __str__(self):
        return self.title


class WorkshopMessage(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=primary_key)
    workshop = models.ForeignKey('codepot.Workshop')
    message = models.TextField(blank=False)

    def __str__(self):
        return '{} / {}'.format(self.workshop.title, self.id)

#TODO mentor can't attend to own workshop
#TODO no one can sign for single workshop more than once
#TODO it impossible to sign for two workshops in a single slot
