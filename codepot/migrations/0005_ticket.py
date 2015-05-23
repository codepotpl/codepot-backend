# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import codepot


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0004_auto_20150523_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.CharField(max_length=32, serialize=False, primary_key=True, default=codepot.create_hash)),
                ('purchase', models.ForeignKey(to='codepot.Purchase')),
            ],
        ),
    ]
