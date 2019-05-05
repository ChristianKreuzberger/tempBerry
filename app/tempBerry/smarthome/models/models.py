from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_userforeignkey.models.fields import UserForeignKey

__all__ = [
    "SmartHome",
    "SmartHomeApiKey",
    "Room",
    "Sensor",
    "SensorIdToSensorMapping",
]


class SmartHome(models.Model):
    """
    A SmartHome contains several smart devices, sensors, etc...
    """
    name = models.CharField(
        max_length=256,
        verbose_name=_("Name of the smart home")
    )

    description = models.TextField(
        verbose_name=_("Additional information for the smart home")
    )

    address = models.CharField(
        max_length=256,
        verbose_name=_("Address of the smart home (e.g., used for weather information)")
    )

    created_by = UserForeignKey(
        auto_user_add=True,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Smart Home")
        verbose_name_plural = _("Smart Homes")

    def __str__(self):
        return self.name


class SmartHomeApiKey(models.Model):
    """
    API Key that has certain access to a smart home
    """
    ACCESS_TYPE_CHOICES = (
        ("read", _("Read only access")),
        ("read_write", _("Read and write access")),
        ("disabled", _("No access")),
    )

    access_type = models.CharField(
        choices=ACCESS_TYPE_CHOICES,
        default="disabled",
        max_length=16,
        verbose_name=_("Access Type for the API Key")
    )

    key = models.CharField(
        max_length=128,
        default="",
        verbose_name=_("API Key")
    )

    smarthome = models.ForeignKey(
        'smarthome.SmartHome',
        related_name='api_keys',
        verbose_name=_("Smart Home that this API Key belongs to")
    )

    class Meta:
        unique_together = (
            ('key', 'smarthome')
        )
        verbose_name = _("API Key")
        verbose_name_plural = _("API Keys")


class Room(models.Model):
    """ A room """

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ("created_at", )

    smarthome = models.ForeignKey(
        'smarthome.SmartHome',
        verbose_name=_("Smart Home that this Room belongs to"),
        blank=True,
        null=True,
        related_name='rooms'
    )

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


class Sensor(models.Model):
    """
    Any type of sensor based on the room
    """
    class Meta:
        verbose_name = _("Sensor")
        verbose_name_plural = _("Sensors")
        ordering = ("room", "created_at", "name")

    SENSOR_AIRPRESSURE = 'air_pressure'
    SENSOR_CAMERA = 'camera'
    SENSOR_DOOR = 'door'
    SENSOR_TEMPERATURE = 'temperature'
    SENSOR_WINDOW = 'window'
    SENSOR_MAIN_DOOR = 'main_door'
    SENSOR_MOVEMENT = 'movement'
    SENSOR_NETWORK_SPEED = 'network_speed'

    SENSOR_CHOICES = (
        (SENSOR_AIRPRESSURE, _('Air Pressure'), ),
        (SENSOR_CAMERA, _('Camera'), ),
        (SENSOR_DOOR, _('Door'),),
        (SENSOR_TEMPERATURE, _('Temperature'), ),
        (SENSOR_WINDOW, _('Window'), ),
        (SENSOR_MAIN_DOOR, _('Main Door'), ),
        (SENSOR_MOVEMENT, _('Movement'), ),
        (SENSOR_NETWORK_SPEED, _('Network Speed'), ),
    )

    room = models.ForeignKey(
        'smarthome.Room',
        verbose_name=_("Room that this label belongs to"),
        blank=True,
        null=True,
        related_name='sensors'
    )

    name = models.CharField(
        max_length=128,
        verbose_name=_("Name of the sensor")
    )

    created_at = models.DateTimeField(
        auto_created=True,
        auto_now_add=True,
        auto_now=False,
        verbose_name=_("When was this sensor created")
    )

    last_updated_at = models.DateTimeField(
        auto_created=True,
        auto_now=True,
        verbose_name=_("When was this sensor config was last updated")
    )

    comment = models.TextField(
        verbose_name=_("Comment for this sensor"),
        blank=True,
        null=True
    )

    public = models.BooleanField(
        verbose_name=_("Whether this sensor is public or not"),
        default=False,
        db_index=True,
    )

    type = models.CharField(
        choices=SENSOR_CHOICES,
        max_length=24,
        db_index=True,
        verbose_name=_("Type of the sensor")
    )

    def __str__(self):
        return "{}/{}".format(self.room, self.name)


class SensorIdToSensorMapping(models.Model):
    """
    Contains a mapping between sensors and (volatile) sensor ids
    Such a mapping has a start and end date, a sensor id and a sensor that is mapped to
    """
    class Meta:
        verbose_name = _("Mapping between sensor and sensor id")
        verbose_name_plural = _("Mappings between sensors and sensor ids")

    real_sensor = models.ForeignKey(
        "smarthome.Sensor",
        related_name="sensor_ids"
    )

    sensor_id = models.IntegerField(
        db_index=True,
        verbose_name=_("The sensor id that the sensor is mapped to"),
    )

    start_date = models.DateTimeField(
        auto_created=False, auto_now=False, auto_now_add=False,
        verbose_name=_("Date time after when this mapping is valid")
    )

    end_date = models.DateTimeField(
        auto_created=False, auto_now=False, auto_now_add=False,
        blank=True, null=True,
        verbose_name=_("Date time until when this mapping is valid")
    )

    def __str__(self):
        return "Sensor {} is mapped to sensor with id {}".format(self.real_sensor, self.sensor_id)
