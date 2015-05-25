# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0006_auto_20150523_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocode',
            name='contact_info',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
