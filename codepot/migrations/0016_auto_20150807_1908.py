# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codepot', '0015_auto_20150807_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField()),
                ('max_attendees', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], default=50)),
                ('attendees', models.ManyToManyField(related_name='attendees', to=settings.AUTH_USER_MODEL)),
                ('mentors', models.ManyToManyField(related_name='mentors', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='codepot.WorkshopTag')),
            ],
        ),
        migrations.AddField(
            model_name='timeslot',
            name='workshop',
            field=models.ForeignKey(default=None, to='codepot.Workshop'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together=set([('room_no', 'timeslot_tier'), ('workshop', 'timeslot_tier')]),
        ),
        migrations.AddField(
            model_name='workshopmessage',
            name='workshop',
            field=models.ForeignKey(default=None, to='codepot.Workshop'),
            preserve_default=False,
        ),
    ]
