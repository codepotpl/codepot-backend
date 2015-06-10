# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0011_auto_20150608_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')], max_length=32, default='PENDING'),
        ),
    ]
