# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import codepot


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codepot', '0002_auto_20150523_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purchase_id', models.CharField(max_length=32, primary_key=True, default=codepot.create_hash, serialize=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
