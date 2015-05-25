# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0009_ticket_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='purchase',
            field=models.OneToOneField(to='codepot.Purchase'),
        ),
    ]
