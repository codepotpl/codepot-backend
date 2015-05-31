# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0009_auto_20150531_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='type',
            field=models.CharField(default=None, choices=[('PAYU', 'PAYU'), ('TRANSFER', 'TRANSFER')], max_length=64),
            preserve_default=False,
        ),
    ]
