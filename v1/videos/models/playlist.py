import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified
from django.contrib.postgres.fields import ArrayField


class Playlist(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    playlist_id = models.CharField(max_length=11)
    items = ArrayField(models.CharField(max_length=11))
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    published_at = models.CharField(max_length=15)
    author = models.CharField(max_length=250)
    thumbnail = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    playlist_type = models.CharField(max_length=15, default='youtube', editable=False)

    class Meta:
        ordering = ('published_at',)
