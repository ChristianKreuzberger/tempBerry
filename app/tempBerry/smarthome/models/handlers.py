import logging

from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from django.dispatch import receiver
from django.core.cache import cache
from django.core.validators import ValidationError
from django.utils.timezone import datetime
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _

from tempBerry.smarthome.models import SensorIdToSensorMapping

# Get an instance of a logger
logger = logging.getLogger(__name__)


__all__ = [
    'verify_sensor_id_unique',
    'set_rooms_on_data_entries_with_sensor_id',
    'auto_set_assigned_sensor_based_on_mapping',
    'update_last_sensor_data_in_cache',
]


@receiver(pre_save, sender=SensorIdToSensorMapping)
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

    mapping = SensorIdToSensorMapping.objects.filter(
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


@receiver(post_save, sender=SensorIdToSensorMapping)
def set_rooms_on_data_entries_with_sensor_id(instance, *args, **kwargs):
    """
    If a room sensor id mapping was changed, check all data entries from start_date to end_date and assign the real
    sensor according to the sensor id mapping
    :param instance:
    :param args:
    :param kwargs:
    :return:
    """

    def _update_sensor_for_data_entry_class(DataEntryCls):
        # get all entries for the given sensor id that do not have an actual sensor
        qs = DataEntryCls.objects.filter(sensor_id=instance.sensor_id, real_sensor__isnull=True)

        # filter by start-date
        qs = qs.filter(created_at__gte=instance.start_date)

        # filter by end_date
        if instance.end_date:
            qs = qs.filter(created_at__lte=instance.end_date)

        # update room for the given entries
        qs.update(real_sensor=instance.real_sensor)

    # ToDo: get all subclasses of AbstractDataEntry
    # for now we just import them manually

    from tempBerry.temperatures.models import TemperatureDataEntry
    _update_sensor_for_data_entry_class(TemperatureDataEntry)

    from tempBerry.binarySensor.models import BinarySensorData
    _update_sensor_for_data_entry_class(BinarySensorData)


@receiver(pre_save)
def auto_set_assigned_sensor_based_on_mapping(instance, sender, raw, *args, **kwargs):
    """
    For each class that inherits from AbstractDataEntry we need to set the real_sensor based on the sensor id mapping
    :param instance:
    :param sender:
    :param args:
    :param kwargs:
    :return:
    """
    if raw:
        return

    from tempBerry.smarthome.models import AbstractDataEntry

    if not isinstance(instance, AbstractDataEntry):
        # not a subclass of AbstractDataEntry - ignore it
        return

    if instance.real_sensor_id:
        # real sensor id is already set - no need to continue here
        return

    # verify that there is a mapping for this sensor id for the current time
    sensor_id = instance.sensor_id

    now = datetime.utcnow().replace(tzinfo=utc)

    # try to get a real_sensor for the given sensor id, where start_date <= now() <= end_date
    mapping = SensorIdToSensorMapping.objects.filter(
        sensor_id=sensor_id,
    ).filter(
        Q(start_date__lte=now, end_date__gte=now) | Q(start_date__lte=now, end_date__isnull=True)
    )

    if len(mapping) == 1:
        # perfect match
        mapping = mapping.first()

        # set instances real sensor id based on the mapping
        instance.real_sensor_id = mapping.real_sensor_id
        instance.room_id = mapping.real_sensor.room_id

        # no need to call .save() here, as we are still within the pre_save phase

    elif len(mapping) > 1:
        # multiple matches, this is not good
        logger.error("Found multiple sensor id mappings for sensor id {}".format(sensor_id))
        return
    else: # len = 0
        # no match, doesnt matter -> this is either false sensor data or something else went wrong
        pass


@receiver(post_save)
def update_last_sensor_data_in_cache(instance, created, *args, **kwargs):
    """
    Stores the latest temperature data in django cache
    :param instance:
    :param created:
    :param args:
    :param kwargs:
    :return:
    """
    # ignore updates
    if not created:
        return

    from tempBerry.smarthome.models import AbstractDataEntry

    if not isinstance(instance, AbstractDataEntry):
        # not a subclass of AbstractDataEntry - ignore it
        return

    # ignore instances that do not have a room_id set
    if not instance.room_id:
        return

    if not instance.sensor_id:
        # skip data without sensor id
        return

    # fetch up2date last_sensor_data
    cached_data = cache.get('last_sensor_data')
    if not cached_data:
        cached_data = dict()

    # cache data by sensor id
    cached_data[instance.real_sensor_id] = instance

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

    cache.set('last_sensor_data', cached_data)
