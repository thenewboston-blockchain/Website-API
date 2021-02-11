import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Playlist(CreatedModified):
    PLAYLIST_TYPE = [
        ('youtube', 'youtube'),
        ('vimeo', 'vimeo')
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    playlist_id = models.CharField(max_length=50, blank=False)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField()
    author = models.CharField(max_length=250)
    thumbnail = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    playlist_type = models.CharField(max_length=15, choices=PLAYLIST_TYPE)

    class Meta:
        ordering = ('published_at',)
