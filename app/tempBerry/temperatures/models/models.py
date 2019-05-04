# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tempBerry.smarthome.models import AbstractDataEntry


class RoomSensorIdMapping(models.Model):
    """ Contains a mapping between rooms and sensor ids"""
    class Meta:
        verbose_name = _("Mapping between room and sensor id")
        verbose_name_plural = _("Mappings between rooms and sensor ids")

    room = models.ForeignKey(
        "smarthome.Room",
        related_name="sensor_id_mappings"
    )

    sensor_id = models.IntegerField(
        db_index=True
    )

    start_date = models.DateTimeField(
        auto_created=False, auto_now=False, auto_now_add=False,
        verbose_name=_("Date time after when this mapping is valid")
    )

    end_date = models.DateTimeField(
        auto_created=False, auto_now=False, auto_now_add=False,
        blank=True, null=True,
        verbose_name=_("Date time until when this mappingi s valid")
    )

    def __str__(self):
        return "Room {} is mapped to sensor with id {}".format(self.room, self.sensor_id)


class TemperatureDataEntry(AbstractDataEntry):
    """ A temperature entry """
    class Meta:
        ordering = ('sensor_id', 'created_at')

    sensor_id = models.IntegerField(
        db_index=True
    )

    temperature = models.FloatField(
        null=True,
        verbose_name=_("Temeprature in Celsius")
    )

    humidity = models.FloatField(
        null=True,
        verbose_name=_("Relative humidify")
    )

    air_pressure = models.FloatField(
        null=True,
        verbose_name=_("Air pressure in PA")
    )

    battery = models.SmallIntegerField(
        null=True,
        verbose_name=_("Battery status of the sensor")
    )

    def __str__(self):
        return "{sensor_id}: {temperature} °C, {humidity} %, {air_pressure} PA // captured at {created_at}".format(
            sensor_id=self.sensor_id,
            temperature=self.temperature,
            humidity=self.humidity,
            air_pressure=self.air_pressure,
            created_at=self.created_at
        )


class UnknownDataEntry(AbstractDataEntry):
    raw_data = models.TextField()


