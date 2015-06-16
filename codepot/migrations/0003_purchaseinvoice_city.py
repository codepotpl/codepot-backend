# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0002_purchaseinvoice_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseinvoice',
            name='city',
            field=models.CharField(max_length=256, default=None),
            preserve_default=False,
        ),
    ]
