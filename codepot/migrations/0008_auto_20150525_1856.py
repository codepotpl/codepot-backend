# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0007_promocode_contact_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promocode',
            old_name='discount_percent',
            new_name='discount',
        ),
        migrations.RemoveField(
            model_name='promocode',
            name='already_used',
        ),
        migrations.AddField(
            model_name='promocode',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
