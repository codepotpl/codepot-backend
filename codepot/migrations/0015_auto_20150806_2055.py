# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0014_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='room_no',
            field=models.CharField(max_length=10),
        ),
    ]
