# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import codepot


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0009_auto_20150715_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, default=codepot.primary_key)),
                ('room_no', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('timeslot_tier', models.ForeignKey(to='codepot.TimeSlotTier')),
            ],
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='room_no',
        ),
        migrations.RemoveField(
            model_name='workshop',
            name='timeslots',
        ),
        migrations.AddField(
            model_name='timeslot',
            name='workshop',
            field=models.ForeignKey(to='codepot.Workshop'),
        ),
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together=set([('room_no', 'timeslot_tier')]),
        ),
    ]
