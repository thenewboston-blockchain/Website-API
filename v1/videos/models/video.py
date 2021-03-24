import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Video(CreatedModified):
    VIDEO_TYPE = [
        ('youtube', 'youtube'),
        ('vimeo', 'vimeo')
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    playlist = models.ForeignKey('videos.Playlist', blank=True, null=True, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=11, blank=False)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField()
    duration = models.PositiveIntegerField()
    author = models.CharField(max_length=250)
    tags = ArrayField(models.CharField(max_length=250, null=True), size=500, default=list, blank=True)
    category = ArrayField(models.CharField(max_length=250, null=True), default=list, blank=True)
    thumbnail = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    video_type = models.CharField(max_length=15, choices=VIDEO_TYPE,)

    class Meta:
        default_related_name = 'videos'
        ordering = ('published_at',)
