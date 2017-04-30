# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.utils.timezone import datetime
from django.utils.timezone import timedelta
from django.utils.timezone import utc


class DataEntry(models.Model):
    """ An abstract data entry """

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
    class Meta:
        ordering=('sensor_id', 'created_at')

    sensor_id = models.IntegerField(
        db_index=True
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


@receiver(post_save, sender=TemperatureDataEntry)
def update_last_temperature_data_in_cache(instance, *args, **kwargs):
    """
    Stores the latest temperature data in django cache
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    cached_data = cache.get('last_temperature_data')
    if not cached_data:
        cached_data = dict()

    cached_data[instance.sensor_id] = instance

    now = datetime.utcnow().replace(tzinfo=utc)

    keys_to_remove = []

    # iterate over all data in cached_data and remove entries older than 3 hours
    for key, entry in cached_data.items():
        timediff = now - entry.created_at
        seconds = timediff.total_seconds()
        if seconds > 60*60*3:
            keys_to_remove.append(key)

    for k in keys_to_remove:
        del cached_data[k]

    cache.set('last_temperature_data', cached_data)

class UnknownDataEntry(DataEntry):
    raw_data = models.TextField()


