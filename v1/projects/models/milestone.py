import uuid

from django.core.cache import cache
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Milestone(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f'#{self.pk}: {self.number}'

    class Meta:
        ordering = ('created_date', 'number')

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(Milestone, self).save(*args, **kwargs)
