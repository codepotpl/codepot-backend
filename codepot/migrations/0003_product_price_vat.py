# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0002_purchase_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_vat',
            field=models.FloatField(default=0.23),
        ),
    ]
