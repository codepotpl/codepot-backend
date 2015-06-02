# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import codepot.models.purchases


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0009_auto_20150602_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='payment_status',
            field=models.CharField(default=None, choices=[('PAYU', 'PAYU'), ('TRANSFER', 'TRANSFER'), ('FREE', 'FREE')], max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='id',
            field=models.CharField(primary_key=True, max_length=32, default=codepot.models.purchases._purchase_id_value, serialize=False),
        ),
    ]
