# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0002_auto_20150529_1511'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promocode',
            old_name='promo_code_id',
            new_name='code',
        ),
    ]
