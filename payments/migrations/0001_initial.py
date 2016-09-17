# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-15 18:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ts', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_ts', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('name', models.CharField(max_length=255)),
                ('merch_txn_ref', models.CharField(help_text='Merchant Transaction Reference', max_length=40, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_ts', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_ts', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('batch_scheduled_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('REJECTED', 'REJECTED'), ('APPROVED', 'APPROVED')], default='PENDING', max_length=8)),
                ('status_message', models.TextField(blank=True, null=True)),
                ('transaction_num', models.CharField(blank=True, help_text='Transaction Number', max_length=19, null=True, unique=True)),
                ('card_type', models.CharField(blank=True, choices=[(b'AE', b'American Express'), (b'AP', b'American Express Corporate Purchase Card'), (b'DC', b'Diners Club'), (b'GC', b'GAP Inc. card'), (b'XX', b'Generic Card'), (b'JC', b'JCB Card'), (b'LY', b'Loyalty Card'), (b'MS', b'Maestro Card'), (b'MC', b'MasterCard'), (b'MX', b'Mondex Card'), (b'PL', b'PLC Card'), (b'SD', b'SafeDebit Card'), (b'SO', b'SOLO Card'), (b'ST', b'STYLE Card'), (b'SW', b'SWITCH Card'), (b'VD', b'Visa Debit Card'), (b'VC', b'Visa Card'), (b'VP', b'Visa Corporate Purchase Card'), (b'EB', b'Electronic Benifit Card')], max_length=2, null=True)),
                ('receipt_no', models.CharField(blank=True, help_text='Receipt Number', max_length=12, null=True, unique=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]