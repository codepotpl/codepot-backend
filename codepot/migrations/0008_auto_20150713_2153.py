# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings
import codepot.models.workshops


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codepot', '0007_auto_20150706_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.CharField(serialize=False, max_length=32, default=codepot.models.workshops._primary_key, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField()),
                ('max_attendees', models.IntegerField(default=50, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('attendee', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('workshop', models.ForeignKey(to='codepot.Workshop')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopMentor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('mentor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('workshop', models.ForeignKey(to='codepot.Workshop')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopMessage',
            fields=[
                ('id', models.CharField(serialize=False, max_length=32, default=codepot.models.workshops._primary_key, primary_key=True)),
                ('message', models.TextField()),
                ('workshop', models.ForeignKey(to='codepot.Workshop')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopTag',
            fields=[
                ('name', models.CharField(serialize=False, max_length=256, primary_key=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='workshop',
            name='tags',
            field=models.ManyToManyField(to='codepot.WorkshopTag'),
        ),
        migrations.AlterUniqueTogether(
            name='workshopmentor',
            unique_together=set([('mentor', 'workshop')]),
        ),
        migrations.AlterUniqueTogether(
            name='workshopattendee',
            unique_together=set([('attendee', 'workshop')]),
        ),
    ]
