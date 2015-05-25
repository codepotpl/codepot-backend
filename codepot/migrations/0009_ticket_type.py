# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0008_auto_20150525_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='type',
            field=models.CharField(default=None, choices=[('FIRST_DAY', 'FIRST_DAY'), ('SECOND_DAY', 'SECOND_DAY'), ('BOTH_DAYS', 'BOTH_DAYS')], max_length=64),
            preserve_default=False,
        ),
    ]
