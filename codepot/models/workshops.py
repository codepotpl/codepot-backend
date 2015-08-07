import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from codepot import primary_key


class WorkshopTag(models.Model):
    name = models.CharField(primary_key=True, max_length=256, blank=False, unique=True)

    def __str__(self):
        return self.name

class Workshop(models.Model):
  title = models.CharField(max_length=512, blank=False)
  description = models.TextField(blank=False)
  tags = models.ManyToManyField('codepot.WorkshopTag', blank=True)
  mentors = models.ManyToManyField(User, related_name='mentors', blank=True)
  attendees = models.ManyToManyField(User, related_name='attendees', blank=True)
  max_attendees = models.IntegerField(default=50, validators=[MinValueValidator(0)], blank=False)

  def __str__(self):
    return self.title


class WorkshopMessage(models.Model):
    id = models.CharField(primary_key=True, max_length=32, default=primary_key)
    workshop = models.ForeignKey('codepot.Workshop')
    author = models.ForeignKey(User)
    message = models.TextField(blank=False)
    created = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)

    def __str__(self):
        return '{} / {}'.format(self.workshop.title, self.id)
