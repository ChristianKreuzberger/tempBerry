from django.db import models


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
    sensor_id = models.IntegerField(
        db_index=True
    )

    temperature = models.FloatField()

    humidity = models.FloatField()

    battery = models.SmallIntegerField()


class UnknownDataEntry(DataEntry):
    raw_data = models.TextField()
