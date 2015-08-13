# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import codepot.models.workshops
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codepot', '0007_auto_20150706_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, default=codepot.primary_key, primary_key=True)),
                ('title', models.CharField(max_length=512)),
                ('description', models.TextField()),
                ('max_attendees', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], default=50)),
                ('attendees', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='attendees')),
                ('mentors', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='mentors')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopMessage',
            fields=[
                ('id', models.CharField(max_length=32, serialize=False, default=codepot.primary_key, primary_key=True)),
                ('message', models.TextField()),
                ('workshop', models.ForeignKey(to='codepot.Workshop')),
            ],
        ),
        migrations.CreateModel(
            name='WorkshopTag',
            fields=[
                ('name', models.CharField(max_length=256, serialize=False, unique=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='workshop',
            name='tags',
            field=models.ManyToManyField(to='codepot.WorkshopTag'),
        ),
    ]
