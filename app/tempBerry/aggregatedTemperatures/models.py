from django.db import models


class HourlyAggregatedTemperature(models.Model):
    sensor_id = models.IntegerField(
        db_index=True
    )

    datetime_day = models.DateField(
        "The day where this entry is calculated for",
        db_index=True
    )

    datetime_hour = models.IntegerField(
        "The hour this entry is calculated for",
        db_index=True
    )

    average_temperature = models.FloatField(
        "Average Temperature"
    )

    average_humidity = models.FloatField(
        "Average Humidity"
    )


