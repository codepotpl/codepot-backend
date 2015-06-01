# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0006_auto_20150601_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='notes',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
