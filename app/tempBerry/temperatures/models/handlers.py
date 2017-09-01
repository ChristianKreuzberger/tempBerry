from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.utils.timezone import datetime
from django.utils.timezone import timedelta
from django.utils.timezone import utc

from tempBerry.temperatures.models.models import TemperatureDataEntry, Room


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

@receiver(pre_save, sender=TemperatureDataEntry)
def store_room_sensor_id_combination(instance, *args, **kwargs):
    """
    Checks if a room already exists,e lse it creates a new room for a temperature data entry
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """

    # verify that there is a room for this sensor id
    sensor_id = instance.sensor_id

    rooms = Room.objects.filter(sensor_id=sensor_id)

    if rooms.exists():
        room = rooms.first()
    else:
        room = Room.objects.create(
            name="Unknown room",
            sensor_id = sensor_id
        )

    instance.room = room