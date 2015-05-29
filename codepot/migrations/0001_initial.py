# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import codepot
import codepot.models.promo_codes
from django.conf import settings
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('djangopay', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('date_from', models.DateTimeField(unique=True)),
                ('date_to', models.DateTimeField(unique=True)),
                ('tickets_purchased', models.IntegerField(default=0)),
                ('both_days', models.ForeignKey(unique=True, to='djangopay.Product', related_name='+')),
                ('first_day', models.ForeignKey(unique=True, to='djangopay.Product', related_name='+')),
                ('second_day', models.ForeignKey(unique=True, to='djangopay.Product', related_name='+')),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('promo_code_id', models.CharField(serialize=False, max_length=6, primary_key=True, default=codepot.models.promo_codes._promo_code_value)),
                ('usage_limit', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1)),
                ('active', models.BooleanField(default=True)),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], default=10)),
                ('sent', models.BooleanField(default=False)),
                ('contact_info', models.TextField(blank=True, null=True, default=None)),
                ('notes', models.TextField(blank=True, null=True, default=None)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('valid_from', models.DateField(blank=True, null=True, default=None)),
                ('valid_to', models.DateField(blank=True, null=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCodeClassification',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purchase_id', models.CharField(serialize=False, max_length=32, primary_key=True, default=codepot.create_hash)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('promo_code', models.ForeignKey(null=True, blank=True, default=None, to='codepot.PromoCode')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.CharField(serialize=False, max_length=32, primary_key=True, default=codepot.create_hash)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('type', models.CharField(choices=[('FIRST_DAY', 'FIRST_DAY'), ('SECOND_DAY', 'SECOND_DAY'), ('BOTH_DAYS', 'BOTH_DAYS')], max_length=64)),
                ('purchase', models.OneToOneField(to='codepot.Purchase')),
            ],
        ),
        migrations.AddField(
            model_name='promocode',
            name='classification',
            field=models.ForeignKey(null=True, blank=True, to='codepot.PromoCodeClassification'),
        ),
    ]
