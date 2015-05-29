# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('djangopay', '0001_initial'),
        ('codepot', '0003_auto_20150530_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='payment',
            field=models.OneToOneField(blank=True, null=True, default=None, to='djangopay.Payment'),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='usage_limit',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
