# -*- coding: utf-8 -*-
from django.db import models


class Room(models.Model):
    """ A room """

    class Meta:
        ordering = ("created_at", )

    name = models.CharField(
        max_length=128,
        verbose_name="Name of the room"
    )

    created_at = models.DateTimeField(
        auto_created=True,
        auto_now=True,
        verbose_name="When was this room created"
    )

    comment = models.TextField(
        verbose_name="Comment for this room"
    )

    sensor_id = models.IntegerField(
        db_index=True,
        verbose_name="Sensor ID related to this room"
    )

    public = models.BooleanField(
        verbose_name="Whether this room is public or not",
        default=False
    )

    def __str__(self):
        return self.name


class DataEntry(models.Model):
    """ An abstract data entry """

    class Meta:
        ordering = ("creatd_at", )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="When was this entry created at"
    )

    source = models.CharField(
        max_length=128,
        verbose_name="Where is this entry from"
    )

    class Meta:
        abstract = True


class TemperatureDataEntry(DataEntry):
    """ A temperature entry """
    class Meta:
        ordering = ('sensor_id', 'created_at')

    sensor_id = models.IntegerField(
        db_index=True
    )

    room = models.ForeignKey(
        "Room",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="The room associated to the temperature data entry"
    )

    temperature = models.FloatField()

    humidity = models.FloatField()

    battery = models.SmallIntegerField()

    def __str__(self):
        return "{sensor_id}: {temperature} °C, {humidity} %".format(
            sensor_id=self.sensor_id,
            temperature=self.temperature,
            humidity=self.humidity
        )


class UnknownDataEntry(DataEntry):
    raw_data = models.TextField()


