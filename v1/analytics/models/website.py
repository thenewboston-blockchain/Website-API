import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Website(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    users = models.PositiveIntegerField()
    sessions = models.PositiveIntegerField()
    bounce_rate = models.FloatField()
    session_duration = models.PositiveIntegerField()
    week_ending = models.DateTimeField()

    class Meta:
        ordering = ('week_ending',)
        verbose_name_plural = 'website'
