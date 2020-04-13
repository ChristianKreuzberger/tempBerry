from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from django.dispatch import receiver
from django.core.cache import cache
from django.core.validators import ValidationError
from django.utils.timezone import datetime
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _

from tempBerry.temperatures.models.models import TemperatureDataEntry, RoomSensorIdMapping


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
