# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import codepot


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0008_auto_20150602_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.CharField(serialize=False, max_length=32, default=codepot.create_hash, primary_key=True),
        ),
    ]
