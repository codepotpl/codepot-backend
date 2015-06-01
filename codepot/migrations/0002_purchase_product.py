# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='product',
            field=models.ForeignKey(to='codepot.Product', default=None),
            preserve_default=False,
        ),
    ]
