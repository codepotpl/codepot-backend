# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0014_auto_20150612_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='final_price',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
