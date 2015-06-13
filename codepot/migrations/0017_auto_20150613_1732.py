# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0016_auto_20150613_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
