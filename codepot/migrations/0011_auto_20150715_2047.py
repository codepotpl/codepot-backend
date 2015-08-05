# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0010_auto_20150715_2018'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together=set([('room_no', 'timeslot_tier'), ('workshop', 'timeslot_tier')]),
        ),
    ]
