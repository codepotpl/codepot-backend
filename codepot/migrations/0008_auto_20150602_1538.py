# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0007_purchase_notes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='type',
            new_name='payment_type',
        ),
    ]
