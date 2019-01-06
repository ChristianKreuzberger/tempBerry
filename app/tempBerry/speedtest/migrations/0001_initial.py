# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-06 17:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('smarthome', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeedtestEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('download_speed', models.FloatField()),
                ('upload_speed', models.FloatField()),
                ('ping', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='When this Speedtest Entry was created')),
                ('smarthome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smarthome.SmartHome', verbose_name='Smart Home that this Speedtest Entry belongs to')),
            ],
            options={
                'verbose_name': 'Speedtest Entry',
                'verbose_name_plural': 'Speedtest Entries',
                'ordering': ('created_at',),
            },
        ),
    ]
