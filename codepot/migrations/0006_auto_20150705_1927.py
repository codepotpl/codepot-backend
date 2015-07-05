# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import codepot.models.promo_codes


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0005_extend_username_field'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appsettings',
            options={'verbose_name': 'App Settings', 'verbose_name_plural': 'App Settings'},
        ),
        migrations.AlterField(
            model_name='promocode',
            name='code',
            field=models.CharField(max_length=20, default=codepot.models.promo_codes._promo_code_value, primary_key=True, serialize=False),
        ),
    ]
