# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0005_remove_product_price_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='payment',
            new_name='payu_payment',
        ),
    ]
