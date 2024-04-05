import uuid

from django.db import models


class UUIDMixin(models.Model):
    """ Reusable uuid field"""

    uuid = models.UUIDField(
        editable=False,
        primary_key=True,
        default=uuid.uuid4
    )

    class Meta:
        abstract = True