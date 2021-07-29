# Generated by Django 2.2.18 on 2021-07-29 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('smarthome', '0004_lat_long'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherForecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True, db_index=True, verbose_name='When was this entry created at')),
                ('json_data', models.TextField()),
                ('source', models.CharField(max_length=128, verbose_name='Where is this entry from')),
                ('smarthome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smarthome.SmartHome', verbose_name='Smart Home that this Weather Forecast belongs to')),
            ],
        ),
    ]
