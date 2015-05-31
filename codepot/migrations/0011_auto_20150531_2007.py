# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0010_purchase_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='type',
            field=models.CharField(choices=[('PAYU', 'PAYU'), ('TRANSFER', 'TRANSFER'), ('FREE', 'FREE')], max_length=64),
        ),
    ]
