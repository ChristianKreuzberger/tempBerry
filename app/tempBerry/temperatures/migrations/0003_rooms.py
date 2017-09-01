# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-02 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('temperatures', '0002_temperature_data_ordering'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now=True, verbose_name='When was this room created')),
                ('name', models.CharField(max_length=128, verbose_name='Name of the room')),
                ('comment', models.TextField(verbose_name='Comment for this room')),
                ('sensor_id', models.IntegerField(db_index=True, verbose_name='Sensor ID related to this room')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.AddField(
            model_name='temperaturedataentry',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='temperatures.Room', verbose_name='The room associated to the temperature data entry'),
        ),
    ]