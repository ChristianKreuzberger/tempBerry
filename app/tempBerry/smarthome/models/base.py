from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = [
    'AbstractDataEntry'
]


class AbstractDataEntry(models.Model):
    """ An abstract data entry """

    class Meta:
        ordering = ("created_at", )
        abstract = True

    created_at = models.DateTimeField(
        auto_created=True,
        auto_now_add=True,
        db_index=True,
        verbose_name=_("When was this entry created at")
    )

    source = models.CharField(
        max_length=128,
        verbose_name=_("Where is this entry from")
    )

    room = models.ForeignKey(
        "smarthome.Room",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Which room is this entry associated to")
    )
