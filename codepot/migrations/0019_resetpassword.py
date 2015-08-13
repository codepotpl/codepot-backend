# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import codepot


class Migration(migrations.Migration):
  dependencies = [
    ('codepot', '0018_merge'),
  ]

  operations = [
    migrations.CreateModel(
      name='ResetPassword',
      fields=[
        ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
        ('token', models.CharField(unique=True, default=codepot.create_hash, max_length=32)),
        ('email', models.CharField(unique=True, max_length=256)),
        ('active', models.BooleanField(default=True)),
      ],
    ),
  ]
