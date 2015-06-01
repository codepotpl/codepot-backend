# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import codepot
from django.conf import settings
import codepot.models.promo_codes
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('django_payu', '0002_auto_20150531_1928'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceTier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('date_from', models.DateTimeField(unique=True)),
                ('date_to', models.DateTimeField(unique=True)),
                ('tickets_purchased', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('price_net', models.IntegerField()),
                ('price_total', models.IntegerField()),
                ('price_tier', models.ForeignKey(to='codepot.PriceTier')),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('code', models.CharField(serialize=False, max_length=6, primary_key=True, default=codepot.models.promo_codes._promo_code_value)),
                ('usage_limit', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], default=1)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.CharField(serialize=False, max_length=32, primary_key=True, default=codepot.create_hash)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('invoice_name', models.CharField(blank=True, max_length=256, null=True)),
                ('invoice_street', models.CharField(blank=True, max_length=256, null=True)),
                ('invoice_zip_code', models.CharField(blank=True, max_length=256, null=True)),
                ('invoice_country', models.CharField(blank=True, max_length=256, null=True)),
                ('invoice_tax_id', models.CharField(blank=True, max_length=256, null=True)),
                ('type', models.CharField(max_length=64, choices=[('PAYU', 'PAYU'), ('TRANSFER', 'TRANSFER'), ('FREE', 'FREE')])),
                ('payment', models.OneToOneField(to='django_payu.PayuPayment', default=None, blank=True, null=True)),
                ('promo_code', models.ForeignKey(to='codepot.PromoCode', blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.CharField(serialize=False, max_length=32, primary_key=True, default=codepot.create_hash)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('type', models.CharField(max_length=64, choices=[('FIRST_DAY', 'FIRST_DAY'), ('SECOND_DAY', 'SECOND_DAY'), ('BOTH_DAYS', 'BOTH_DAYS')])),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='ticket',
            field=models.OneToOneField(to='codepot.Ticket'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='promocode',
            name='classification',
            field=models.ForeignKey(to='codepot.PromoCodeClassification', null=True, blank=True),
        ),
    ]
