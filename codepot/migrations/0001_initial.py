# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import codepot
import datetime
import django.core.validators
import codepot.models.purchases
import codepot.models.promo_codes
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_payu', '0003_payupayment_continue_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceTier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('date_from', models.DateTimeField(unique=True)),
                ('date_to', models.DateTimeField(unique=True)),
                ('tickets_purchased', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, default=codepot.create_hash)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('price_net', models.IntegerField()),
                ('price_vat', models.FloatField(default=0.23)),
                ('price_tier', models.ForeignKey(to='codepot.PriceTier')),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False, default=codepot.models.promo_codes._promo_code_value)),
                ('usage_limit', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('active', models.BooleanField(default=True)),
                ('discount', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('sent', models.BooleanField(default=False)),
                ('contact_info', models.TextField(null=True, blank=True, default=None)),
                ('notes', models.TextField(null=True, blank=True, default=None)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('valid_from', models.DateField(null=True, blank=True, default=None)),
                ('valid_to', models.DateField(null=True, blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCodeClassification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, default=codepot.models.purchases._purchase_id_value)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('payment_type', models.CharField(choices=[('PAYU', 'PAYU'), ('TRANSFER', 'TRANSFER'), ('FREE', 'FREE')], max_length=64)),
                ('payment_status', models.CharField(choices=[('PENDING', 'PENDING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')], max_length=32, default='PENDING')),
                ('amount', models.IntegerField(default=0)),
                ('payu_payment_link', models.URLField(max_length=4096, null=True, blank=True, default=None)),
                ('notes', models.TextField()),
                ('payu_payment', models.OneToOneField(null=True, blank=True, to='django_payu.PayuPayment', default=None)),
                ('product', models.ForeignKey(to='codepot.Product')),
                ('promo_code', models.ForeignKey(null=True, blank=True, to='codepot.PromoCode', default=None)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseInvoice',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, default=codepot.models.purchases._purchase_id_value)),
                ('no', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('street', models.CharField(max_length=256)),
                ('zip_code', models.CharField(max_length=256)),
                ('country', models.CharField(max_length=256)),
                ('tax_id', models.CharField(max_length=256)),
                ('purchase', models.OneToOneField(null=True, blank=True, to='codepot.Purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, default=codepot.create_hash)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('type', models.CharField(choices=[('FIRST_DAY', 'FIRST_DAY'), ('SECOND_DAY', 'SECOND_DAY'), ('BOTH_DAYS', 'BOTH_DAYS')], max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='promocode',
            name='classification',
            field=models.ForeignKey(null=True, blank=True, to='codepot.PromoCodeClassification'),
        ),
    ]
