# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0012_auto_20150610_0723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='invoice',
        ),
        migrations.AddField(
            model_name='purchaseinvoice',
            name='purchase',
            field=models.OneToOneField(to='codepot.Purchase', blank=True, null=True),
        ),
    ]
