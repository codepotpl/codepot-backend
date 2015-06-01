# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0004_remove_purchase_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_total',
        ),
    ]
