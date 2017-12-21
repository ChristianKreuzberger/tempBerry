# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Room(models.Model):
    """ A room """

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ("created_at", )

    name = models.CharField(
        max_length=128,
        verbose_name=_("Name of the room")
    )

    created_at = models.DateTimeField(
        auto_created=True,
        auto_now_add=True,
        auto_now=False,
        verbose_name=_("When was this room created")
    )

    last_updated_at = models.DateTimeField(
        auto_created=True,
        auto_now=True,
        verbose_name=_("When was this room last updated")
    )

    comment = models.TextField(
        verbose_name=_("Comment for this room")
    )

    public = models.BooleanField(
        verbose_name=_("Whether this room is public or not"),
        default=False
    )

    has_temperature = models.BooleanField(
        default=False,
        verbose_name=_("Whether this room has a working temperature sensor")
    )

    has_humidity = models.BooleanField(
        default=False,
        verbose_name=_("Whether this room has a working humidity sensor")
    )

    has_air_pressure = models.BooleanField(
        default=False,
        verbose_name=_("Whether this room has a working air pressure sensor")
    )

    def __str__(self):
        return self.name


class RoomSensorIdMapping(models.Model):
    """ Contains a mapping between rooms and sensor ids"""
    class Meta:
        verbose_name = _("Mapping between room and sensor id")
        verbose_name_plural = _("Mappings between rooms and sensor ids")

    room = models.ForeignKey(
        "temperatures.Room",
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


class DataEntry(models.Model):
    """ An abstract data entry """

    class Meta:
        ordering = ("created_at", )
        abstract = True

    created_at = models.DateTimeField(
        auto_created=True,
        auto_now_add=True,
        db_index=True,
        verbose_name=_("When was this entry created at")
    )

    source = models.CharField(
        max_length=128,
        verbose_name=_("Where is this entry from")
    )

    room = models.ForeignKey(
        "temperatures.Room",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Which room is this entry associated to")
    )


class TemperatureDataEntry(DataEntry):
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


class UnknownDataEntry(DataEntry):
    raw_data = models.TextField()


