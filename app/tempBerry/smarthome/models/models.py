from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_userforeignkey.models.fields import UserForeignKey

__all__ = [
    "SmartHome",
    "SmartHomeApiKey",
    "Room",
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
