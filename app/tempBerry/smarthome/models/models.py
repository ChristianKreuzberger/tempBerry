from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_userforeignkey.models.fields import UserForeignKey

__all__ = ["SmartHome"]


class SmartHome(models.Model):
    """
    A SmartHome contains several smart devices
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

    created_by = UserForeignKey()

    created_at = models.DateTimeField(auto_now_add=True)
