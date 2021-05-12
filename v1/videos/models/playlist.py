import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Playlist(CreatedModified):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField()
    instructor = models.ForeignKey('videos.Instructor', on_delete=models.CASCADE, null=True)
    thumbnail = models.CharField(max_length=250)
    categories = models.ManyToManyField('videos.PlaylistCategory')

    class Meta:
        ordering = ('published_at',)
