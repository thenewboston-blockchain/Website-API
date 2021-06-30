import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Community(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    projects_approved = models.PositiveIntegerField()
    projects_completed = models.PositiveIntegerField()
    week_ending = models.DateTimeField()

    class Meta:
        ordering = ('week_ending',)
        verbose_name_plural = 'community'

    def __str__(self):
        return f'#{self.pk}: {self.week_ending}'
