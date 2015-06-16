# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0004_auto_20150616_1820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='amount',
            new_name='price_net',
        ),
        migrations.AddField(
            model_name='purchase',
            name='price_total',
            field=models.IntegerField(default=0),
        ),
    ]
