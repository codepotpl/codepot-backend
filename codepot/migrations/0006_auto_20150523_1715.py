# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0005_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='already_used',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='promocode',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='promocode',
            name='discount_percent',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], default=10),
        ),
        migrations.AddField(
            model_name='promocode',
            name='notes',
            field=models.TextField(null=True, default=None, blank=True),
        ),
        migrations.AddField(
            model_name='promocode',
            name='sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='promocode',
            name='usage_limit',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1),
        ),
        migrations.AddField(
            model_name='promocode',
            name='valid_from',
            field=models.DateField(null=True, default=None, blank=True),
        ),
        migrations.AddField(
            model_name='promocode',
            name='valid_to',
            field=models.DateField(null=True, default=None, blank=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='ticket',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
