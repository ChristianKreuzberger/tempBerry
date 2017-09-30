from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.core.validators import ValidationError
from django.utils.timezone import datetime
from django.utils.timezone import timedelta
from django.utils.timezone import utc

from tempBerry.temperatures.models.models import TemperatureDataEntry, Room, RoomSensorIdMapping


@receiver(post_save, sender=TemperatureDataEntry)
def update_last_temperature_data_in_cache(instance, created, *args, **kwargs):
    """
    Stores the latest temperature data in django cache
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    # ignore instances that do not have a room_id set
    if not instance.room_id:
        return

    # ignore updates
    if not created:
        return

    cached_data = cache.get('last_temperature_data')
    if not cached_data:
        cached_data = dict()

    cached_data[instance.room_id] = instance

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
    Checks if the given sensor_id matches a room
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """

    # ignore this if room id is already set
    if instance.room_id:
        return

    # verify that there is a room for this sensor id
    sensor_id = instance.sensor_id

    now = datetime.utcnow().replace(tzinfo=utc)

    from django.db.models import Q

    # try to get a room for the given sensor id, where start_date <= now() <= end_date
    mapping = RoomSensorIdMapping.objects.filter(
        sensor_id=sensor_id,
    ).filter(
        Q(start_date__lte=now, end_date__gte=now) | Q(start_date__lte=now, end_date__isnull=True)
    )

    if len(mapping) == 1:
        mapping = mapping.first()
        # perfect match
        instance.room_id = mapping.room_id

        # check if data exists in cache
        cached_data = cache.get('last_temperature_data')
        if cached_data and instance.room_id in cached_data:
            last_room_data = cached_data[instance.room_id]
            # check if difference in temperature is plausible
            if abs(last_room_data.temperature - instance.temperature) > 5:
                raise ValidationError(
                    {'temperature': ValidationError(
                        "Temperature changed rapidly, rejecting",
                        params={'temperature': instance.temperature},
                        code='invalid'
                    )}
                )
            elif abs(last_room_data.humidity - instance.humidity) > 30:
                raise ValidationError(
                    {'humidity': ValidationError(
                        "Humidity changed rapidly, rejecting",
                        params={'humidity': instance.humidity},
                        code='invalid'
                    )}
                )
