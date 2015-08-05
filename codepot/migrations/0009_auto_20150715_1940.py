# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import codepot


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0008_auto_20150713_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlotTier',
            fields=[
                ('id', models.CharField(primary_key=True, serialize=False, max_length=32, default=codepot.primary_key)),
                ('date_from', models.DateTimeField()),
                ('date_to', models.DateTimeField()),
                ('day', models.CharField(max_length=16, choices=[('FIRST', 'FIRST'), ('SECOND', 'SECOND')])),
            ],
        ),
        migrations.AddField(
            model_name='workshop',
            name='room_no',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='timeslottier',
            unique_together=set([('date_to', 'date_from', 'day')]),
        ),
        migrations.AddField(
            model_name='workshop',
            name='timeslots',
            field=models.ManyToManyField(to='codepot.TimeSlotTier'),
        ),
    ]
