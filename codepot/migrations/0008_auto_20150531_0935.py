# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0007_purchase_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='both_days',
        ),
        migrations.RemoveField(
            model_name='price',
            name='first_day',
        ),
        migrations.RemoveField(
            model_name='price',
            name='second_day',
        ),
        migrations.AddField(
            model_name='price',
            name='both_days_net',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='both_days_total',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='both_days_vat',
            field=models.FloatField(default=0.23),
        ),
        migrations.AddField(
            model_name='price',
            name='first_day_net',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='first_day_total',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='first_day_vat',
            field=models.FloatField(default=0.23),
        ),
        migrations.AddField(
            model_name='price',
            name='second_day_net',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='second_day_total',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='price',
            name='second_day_vat',
            field=models.FloatField(default=0.23),
        ),
    ]
