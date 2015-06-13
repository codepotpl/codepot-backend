# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0015_purchase_final_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='final_price',
            new_name='amount',
        ),
    ]
