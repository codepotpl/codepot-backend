from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from codepot import create_hash


def _primary_key():
    return create_hash(10)


class WorkshopTag(models.Model):
    name = models.CharField(primary_key=True, max_length=256, blank=False, unique=True)

    def __str__(self):
        return self.name


class Workshop(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=_primary_key)
    title = models.CharField(max_length=512, blank=False)
    description = models.TextField(blank=False)
    max_attendees = models.IntegerField(default=50, validators=[MinValueValidator(0)], blank=False)
    tags = models.ManyToManyField(WorkshopTag)

    def __str__(self):
        return self.title


class WorkshopMessage(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=_primary_key)
    workshop = models.ForeignKey(Workshop)
    message = models.TextField(blank=False)

    def __str__(self):
        return '{} / {}'.format(self.workshop.title, self.id)


class WorkshopMentor(models.Model):
    mentor = models.ForeignKey(User)
    workshop = models.ForeignKey(Workshop)

    class Meta:
        unique_together = ('mentor', 'workshop',)

    def __str__(self):
        return '{} / {} / {}'.format(self.workshop, self.mentor, self.id)


class WorkshopAttendee(models.Model):
    attendee = models.ForeignKey(User)
    workshop = models.ForeignKey(Workshop)

    class Meta:
        unique_together = ('attendee', 'workshop',)

    def __str__(self):
        return '{} / {}'.format(self.workshop, self.attendee)

#TODO mentor can't attend to own workshop
#TODO no one can sign for single workshop more than once
#TODO it impossible to sign for two workshops in a single slot
