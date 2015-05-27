# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0012_auto_20150527_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('date_from', models.DateTimeField(unique=True)),
                ('date_to', models.DateTimeField(unique=True)),
                ('first_day', models.DecimalField(max_digits=4, decimal_places=4, validators=[django.core.validators.MinValueValidator(1)])),
                ('second_day', models.DecimalField(max_digits=4, decimal_places=4, validators=[django.core.validators.MinValueValidator(1)])),
                ('both_days', models.DecimalField(max_digits=4, decimal_places=4, validators=[django.core.validators.MinValueValidator(1)])),
                ('tickets_purchased', models.IntegerField(default=0)),
            ],
        ),
    ]
