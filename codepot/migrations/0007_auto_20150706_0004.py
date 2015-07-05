# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import codepot.models.promo_codes


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0006_auto_20150705_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='code',
            field=models.CharField(serialize=False, default=codepot.models.promo_codes._promo_code_value, validators=[django.core.validators.MinLengthValidator(10)], primary_key=True, max_length=10),
        ),
    ]
