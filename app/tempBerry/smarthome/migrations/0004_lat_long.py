# Generated by Django 2.2.18 on 2021-07-29 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarthome', '0003_plants'),
    ]

    operations = [
        migrations.AddField(
            model_name='smarthome',
            name='latitude',
            field=models.FloatField(null=True, verbose_name='Latitude of location of smart home (e.g., used for weather information)'),
        ),
        migrations.AddField(
            model_name='smarthome',
            name='longitude',
            field=models.FloatField(null=True, verbose_name='Longitude of location of smart home (e.g., used for weather information)'),
        ),
    ]