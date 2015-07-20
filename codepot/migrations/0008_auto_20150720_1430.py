# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0007_auto_20150706_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='payment_type',
            field=models.CharField(max_length=64, choices=[('PAYU', 'PAYU'), ('TRANSFER', 'TRANSFER'), ('FREE', 'FREE'), ('GROUP', 'GROUP')]),
        ),
    ]
