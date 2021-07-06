import uuid

from django.core.cache import cache
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Instructor(CreatedModified):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=250)
    youtube_url = models.URLField(blank=True, null=True)
    vimeo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'#{self.pk}: {self.name}'

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(Instructor, self).save(*args, **kwargs)
