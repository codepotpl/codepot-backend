# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0023_auto_20150813_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslottier',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
