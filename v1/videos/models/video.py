import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Video(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    playlist = models.ForeignKey('videos.Playlist', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField()
    duration_seconds = models.PositiveIntegerField()
    thumbnail = models.CharField(max_length=250)
    position = models.IntegerField()

    class Meta:
        default_related_name = 'videos'
        ordering = ('published_at',)
