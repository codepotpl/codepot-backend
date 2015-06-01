# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0003_product_price_vat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='ticket',
        ),
    ]
