# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0021_workshopmentor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshopmentor',
            name='bio_in_md',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workshopmentor',
            name='first_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='workshopmentor',
            name='github_username',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='workshopmentor',
            name='googleplus_handler',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='workshopmentor',
            name='last_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='workshopmentor',
            name='linkedin_profile_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workshopmentor',
            name='picture_url',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='workshopmentor',
            name='stackoverflow_id',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='workshopmentor',
            name='tagline',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='workshopmentor',
            name='twitter_username',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='workshopmentor',
            name='website_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
