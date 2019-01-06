from django.db import models


class SpeedtestEntry(models.Model):

    smarthome = models.ForeignKey(
        'smarthome.SmartHome'
    )

    download_speed = models.FloatField()
    upload_speed = models.FloatField()
    ping = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
