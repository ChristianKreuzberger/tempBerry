from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from django.dispatch import receiver
from django.core.cache import cache
from django.core.validators import ValidationError
from django.utils.timezone import datetime
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _

from tempBerry.temperatures.models.models import TemperatureDataEntry, RoomSensorIdMapping


@receiver(post_save, sender=TemperatureDataEntry)
def update_last_temperature_data_in_cache(instance, created, *args, **kwargs):
    """
    Stores the latest temperature data in django cache
    :param instance: TemperatureDataEntry
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

    if not instance.sensor_id:
        # skip data without sensor id
        return

    # cache data by sensor id
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


@receiver(pre_save, sender=RoomSensorIdMapping)
def verify_sensor_id_unique(instance, *args, **kwargs):
    """
    Checks that for a given sensor id only one instance is currently active
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """
    # verify that there is a room for this sensor id
    sensor_id = instance.sensor_id

    now = datetime.utcnow().replace(tzinfo=utc)

    mapping = RoomSensorIdMapping.objects.filter(
        sensor_id=sensor_id,
    ).filter(
        Q(start_date__lte=now, end_date__gte=now) | Q(start_date__lte=now, end_date__isnull=True)
    ).exclude(
        # exclude current id
        id=instance.id
    )

    if mapping.exists():
        raise ValidationError({
            "sensor_id": ValidationError(_("There is already an active record for the given sensor id"))
        })


@receiver(post_save, sender=RoomSensorIdMapping)
def set_rooms_on_data_entries_with_sensor_id(instance, *args, **kwargs):
    """
    If a room sensor id mapping was changed, check all data entries from start_date to end_date and move them into the
    room defined by room sensor id mapping
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """

    # get all entries for the given sensor id that do not have a room set
    qs = TemperatureDataEntry.objects.filter(sensor_id=instance.sensor_id, room__isnull=True)

    # filter by start-date
    qs = qs.filter(created_at__gte=instance.start_date)

    # filter by end_date
    if instance.end_date:
        qs = qs.filter(created_at__lte=instance.end_date)

    # update room for the given entries
    qs.update(room=instance.room)


@receiver(pre_save, sender=TemperatureDataEntry)
def store_room_sensor_id_combination(instance, *args, **kwargs):
    """
    When storing a temperature data entry, check if the given sensor_id matches a room
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

    # try to get a room for the given sensor id, where start_date <= now() <= end_date
    mapping = RoomSensorIdMapping.objects.filter(
        sensor_id=sensor_id,
    ).filter(
        Q(start_date__lte=now, end_date__gte=now) | Q(start_date__lte=now, end_date__isnull=True)
    )

    if len(mapping) == 1:
        # perfect match
        mapping = mapping.first()
        instance.room_id = mapping.room_id

        # check if data exists in cache
        cached_data = cache.get('last_temperature_data')

        # update the cache if anything exists
        if cached_data and instance.sensor_id in cached_data:
            last_sensor_data = cached_data[instance.sensor_id]

            # check if difference in temperature is plausible
            if abs(last_sensor_data.temperature - instance.temperature) > 5:
                raise ValidationError(
                    {'temperature': ValidationError(
                        "Temperature changed rapidly, rejecting",
                        params={'temperature': instance.temperature},
                        code='invalid'
                    )}
                )
            elif abs(last_sensor_data.humidity - instance.humidity) > 30:
                raise ValidationError(
                    {'humidity': ValidationError(
                        "Humidity changed rapidly, rejecting",
                        params={'humidity': instance.humidity},
                        code='invalid'
                    )}
                )
