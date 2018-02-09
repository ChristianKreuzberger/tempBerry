# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-21 20:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('temperatures', '0008_auto_datefields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperaturedataentry',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='temperatures.Room', verbose_name='Which room is this entry associated to'),
        ),
        migrations.AlterField(
            model_name='unknowndataentry',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='temperatures.Room', verbose_name='Which room is this entry associated to'),
        ),
    ]