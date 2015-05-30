# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0006_auto_20150530_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='price',
            field=models.ForeignKey(to='codepot.Price', default=None),
            preserve_default=False,
        ),
    ]
