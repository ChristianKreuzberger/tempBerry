from django.db import models
from django.utils.translation import ugettext_lazy as _


class SpeedtestEntry(models.Model):
    """
    A Speedtest Entry is a special sensor that belongs to a smarthome
    """

    smarthome = models.ForeignKey(
        'smarthome.SmartHome',
        verbose_name=_("Smart Home that this Speedtest Entry belongs to"),
        on_delete=models.CASCADE,
    )

    download_speed = models.FloatField()
    upload_speed = models.FloatField()
    ping = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_("When this Speedtest Entry was created")
    )

    class Meta:
        verbose_name = _("Speedtest Entry")
        verbose_name_plural = _("Speedtest Entries")
        ordering = ("created_at", )
