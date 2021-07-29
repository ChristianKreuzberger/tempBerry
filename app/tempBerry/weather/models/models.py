from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = [
    'WeatherForecast'
]

class WeatherForecast(models.Model):
    """
    A Speedtest Entry is a special sensor that belongs to a smarthome
    """

    smarthome = models.ForeignKey(
        'smarthome.SmartHome',
        verbose_name=_("Smart Home that this Weather Forecast belongs to"),
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_created=True,
        auto_now_add=True,
        db_index=True,
        verbose_name=_("When was this entry created at")
    )

    json_data = models.TextField()

    source = models.CharField(
        max_length=128,
        verbose_name=_("Where is this entry from")
    )

