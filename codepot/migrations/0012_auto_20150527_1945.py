# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0011_auto_20150527_1942'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TicketClassification',
            new_name='PromoCodeClassification',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='classification',
        ),
        migrations.AddField(
            model_name='promocode',
            name='classification',
            field=models.ForeignKey(to='codepot.PromoCodeClassification', blank=True, null=True),
        ),
    ]
