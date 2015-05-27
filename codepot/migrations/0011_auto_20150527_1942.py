# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0010_auto_20150525_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='classification',
            field=models.ForeignKey(blank=True, null=True, to='codepot.TicketClassification'),
        ),
    ]
