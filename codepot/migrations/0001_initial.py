# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import codepot
import django.core.validators
from django.conf import settings
import codepot.models.promo_codes
import datetime
import codepot.models.purchases


class Migration(migrations.Migration):

    dependencies = [
        ('django_payu', '0003_payupayment_continue_url'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceTier',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('date_from', models.DateTimeField(unique=True)),
                ('date_to', models.DateTimeField(unique=True)),
                ('tickets_purchased', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(default=codepot.create_hash, max_length=32, serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('price_net', models.IntegerField()),
                ('price_vat', models.FloatField(default=0.23)),
                ('price_tier', models.ForeignKey(to='codepot.PriceTier')),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('code', models.CharField(default=codepot.models.promo_codes._promo_code_value, max_length=6, serialize=False, primary_key=True)),
                ('usage_limit', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('active', models.BooleanField(default=True)),
                ('discount', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('sent', models.BooleanField(default=False)),
                ('contact_info', models.TextField(null=True, default=None, blank=True)),
                ('notes', models.TextField(null=True, default=None, blank=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('valid_from', models.DateField(null=True, default=None, blank=True)),
                ('valid_to', models.DateField(null=True, default=None, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCodeClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.CharField(default=codepot.models.purchases._purchase_id_value, max_length=32, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('payment_type', models.CharField(max_length=64, choices=[('PAYU', 'PAYU'), ('TRANSFER', 'TRANSFER'), ('FREE', 'FREE')])),
                ('payment_status', models.CharField(default='PENDING', max_length=32, choices=[('PENDING', 'PENDING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')])),
                ('amount', models.IntegerField(default=0)),
                ('payu_payment_link', models.URLField(null=True, default=None, max_length=4096, blank=True)),
                ('notes', models.TextField()),
                ('payu_payment', models.OneToOneField(null=True, default=None, blank=True, to='django_payu.PayuPayment')),
                ('product', models.ForeignKey(to='codepot.Product')),
                ('promo_code', models.ForeignKey(null=True, default=None, blank=True, to='codepot.PromoCode')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseInvoice',
            fields=[
                ('id', models.CharField(default=codepot.models.purchases._purchase_id_value, max_length=32, serialize=False, primary_key=True)),
                ('no', models.CharField(null=True, max_length=256, blank=True)),
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
                ('id', models.CharField(default=codepot.create_hash, max_length=32, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('type', models.CharField(max_length=64, choices=[('FIRST_DAY', 'FIRST_DAY'), ('SECOND_DAY', 'SECOND_DAY'), ('BOTH_DAYS', 'BOTH_DAYS')])),
            ],
        ),
        migrations.AddField(
            model_name='promocode',
            name='classification',
            field=models.ForeignKey(null=True, blank=True, to='codepot.PromoCodeClassification'),
        ),
    ]
