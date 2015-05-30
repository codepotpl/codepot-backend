# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0005_auto_20150530_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='ticket_id',
            new_name='id',
        ),
    ]
