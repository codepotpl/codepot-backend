# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0013_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='both_days',
            field=models.DecimalField(validators=[django.core.validators.MinValueValidator(1)], max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='price',
            name='first_day',
            field=models.DecimalField(validators=[django.core.validators.MinValueValidator(1)], max_digits=4, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='price',
            name='second_day',
            field=models.DecimalField(validators=[django.core.validators.MinValueValidator(1)], max_digits=4, decimal_places=2),
        ),
    ]
