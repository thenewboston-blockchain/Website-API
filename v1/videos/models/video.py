import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified
from django.contrib.postgres.fields import ArrayField


class Video(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    video_id = models.CharField(max_length=11)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    published_at = models.CharField(max_length=15)
    duration = models.PositiveIntegerField()
    author = models.CharField(max_length=250)
    tags = ArrayField(models.CharField(max_length=250), size=500, blank=True)
    category = ArrayField(models.CharField(max_length=250), blank=True)
    thumbnail = models.CharField(max_length=250)
    language = models.CharField(max_length=250)
    video_type = models.CharField(max_length=15, default='youtube', editable=False)

    class Meta:
        ordering = ('published_at',)
