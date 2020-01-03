from django.db import models
from django.utils.translation import ugettext_lazy as _


class HourlyAggregatedTemperature(models.Model):
    class Meta:
        ordering = ('-datetime_day', '-datetime_hour')
        unique_together = (
            ('room', 'datetime_day', 'datetime_hour')
        )

    room = models.ForeignKey(
        "smarthome.Room",
        null=True,
        on_delete=models.CASCADE,
    )

    datetime_day = models.DateField(
        verbose_name=_("The day where this entry is calculated for"),
        db_index=True
    )

    datetime_hour = models.IntegerField(
        verbose_name=_("The hour this entry is calculated for"),
        db_index=True
    )

    average_temperature = models.FloatField(
        verbose_name=_("Average Temperature"),
        null=True
    )

    average_humidity = models.FloatField(
        verbose_name=_("Average Humidity"),
        null=True
    )

    average_air_pressure = models.FloatField(
        verbose_name=_("Average Air Pressure"),
        null=True
    )


