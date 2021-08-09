import uuid

from django.core.cache import cache
from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Roadmap(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    team = models.ForeignKey('teams.CoreTeam', on_delete=models.CASCADE)
    task_title = models.CharField(max_length=255)
    estimated_completion_date = models.DateField()
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'#{self.pk}: {self.task_title}'

    class Meta:
        ordering = ('estimated_completion_date',)

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(Roadmap, self).save(*args, **kwargs)
