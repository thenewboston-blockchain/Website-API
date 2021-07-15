import uuid

from django.core.cache import cache
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Responsibility(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'responsibility'
        verbose_name_plural = 'responsibilities'

    def __str__(self):
        return f'#{self.pk}: {self.title}'

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(Responsibility, self).save(*args, **kwargs)
