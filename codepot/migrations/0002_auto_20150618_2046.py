# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='payment_status',
            field=models.CharField(max_length=32, default='PENDING', choices=[('PENDING', 'PENDING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED'), ('STARTED', 'STARTED')]),
        ),
    ]
