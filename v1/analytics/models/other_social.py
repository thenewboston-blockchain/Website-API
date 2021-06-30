import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class OtherSocial(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    discord_members = models.PositiveIntegerField()
    reddit_subscribers = models.PositiveIntegerField()
    youtube_subscribers = models.PositiveIntegerField()
    week_ending = models.DateTimeField()

    class Meta:
        ordering = ('week_ending',)

    def __str__(self):
        return f'#{self.pk}: {self.week_ending}'
