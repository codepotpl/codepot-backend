# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0014_auto_20150806_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshop',
            name='attendees',
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='mentors',
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='workshopmessage',
            name='workshop',
        ),
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='workshop',
        ),
        migrations.DeleteModel(
            name='Workshop',
        ),
    ]
