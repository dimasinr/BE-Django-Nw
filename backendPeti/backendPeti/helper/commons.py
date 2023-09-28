from django.db import models


class TrackableDateModel(models.Model):
    """Abstract model to Track the creation/updated date for a model."""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True