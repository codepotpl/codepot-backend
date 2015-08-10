from django.db import models

from codepot import create_hash


class ResetPassword(models.Model):
  token = models.CharField(max_length=32, blank=False, null=False, unique=True, default=create_hash)
  email = models.CharField(max_length=256, blank=False, null=False, unique=True)
  active = models.BooleanField(default=True)
