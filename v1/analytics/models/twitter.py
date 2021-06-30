import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Twitter(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    tweets = models.PositiveIntegerField()
    tweet_impressions = models.PositiveIntegerField()
    profile_visits = models.PositiveIntegerField()
    mentions = models.PositiveIntegerField()
    total_followers = models.PositiveIntegerField()
    new_followers = models.PositiveIntegerField()
    week_ending = models.DateTimeField()

    class Meta:
        ordering = ('week_ending',)
        verbose_name_plural = 'twitter'

    def __str__(self):
        return f'#{self.pk}: {self.week_ending}'
