# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0026_auto_20150814_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='LimitedWorkshop',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('codepot.workshop',),
        ),
    ]
