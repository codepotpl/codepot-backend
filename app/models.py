from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=128, blank=False, null=False)
    last_name = models.CharField(max_length=128, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False, validators=[EmailValidator])

    def full_name(self):
        return self.first_name + ' ' + self.last_name