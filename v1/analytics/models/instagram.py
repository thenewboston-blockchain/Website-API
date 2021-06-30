import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Instagram(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    account_reached = models.PositiveIntegerField()
    impressions = models.PositiveIntegerField()
    profile_visits = models.PositiveIntegerField()
    website_taps = models.PositiveIntegerField()
    content_interactions = models.PositiveIntegerField()
    followers = models.PositiveIntegerField()
    week_ending = models.DateTimeField()

    class Meta:
        ordering = ('week_ending',)
        verbose_name_plural = 'instagram'

    def __str__(self):
        return f'#{self.pk}: {self.week_ending}'
