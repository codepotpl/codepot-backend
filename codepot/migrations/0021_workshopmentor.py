# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codepot', '0020_auto_20150812_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopMentor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('first_name', models.CharField(blank=True, max_length=256)),
                ('last_name', models.CharField(blank=True, max_length=256)),
                ('tagline', models.CharField(blank=True, max_length=512)),
                ('picture_url', models.CharField(blank=True, max_length=512)),
                ('twitter_username', models.CharField(blank=True, max_length=256)),
                ('github_username', models.CharField(blank=True, max_length=256)),
                ('linkedin_profile_url', models.URLField(blank=True)),
                ('stackoverflow_id', models.CharField(blank=True, max_length=128)),
                ('googleplus_handler', models.CharField(blank=True, max_length=128)),
                ('website_url', models.URLField(blank=True)),
                ('bio_in_md', models.TextField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
