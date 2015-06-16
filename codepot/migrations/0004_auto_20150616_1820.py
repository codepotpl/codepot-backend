# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0003_purchaseinvoice_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
    ]
