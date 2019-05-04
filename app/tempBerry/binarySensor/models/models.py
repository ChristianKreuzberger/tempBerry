from django.db import models

from tempBerry.smarthome.models import AbstractDataEntry

__all__ = [
    'BinarySensorData'
]


class BinarySensorData(AbstractDataEntry):
    """ A binary sensor data entry """
    class Meta:
        ordering = ('sensor_id', 'created_at')

    sensor_id = models.IntegerField(
        db_index=True
    )

    binary_state = models.SmallIntegerField()

    def __str__(self):
        return "{sensor_id}: {binary_state} // captured at {created_at}".format(
            sensor_id=self.sensor_id,
            binary_state=self.binary_state,
            created_at=self.created_at
        )
