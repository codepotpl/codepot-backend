# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0016_auto_20150807_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='attendees',
            field=models.ManyToManyField(related_name='attendees', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='mentors',
            field=models.ManyToManyField(related_name='mentors', blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='tags',
            field=models.ManyToManyField(blank=True, to='codepot.WorkshopTag'),
        ),
    ]
