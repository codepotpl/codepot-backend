# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0004_auto_20150530_1357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='purchase_id',
            new_name='id',
        ),
    ]
