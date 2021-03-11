import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Team(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=250)
    about = models.TextField(blank=True, null=True)
    github = models.URLField(blank=True, null=True, max_length=500)
    slack = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return f'#{self.pk}: {self.title}'

    class Meta:
        ordering = ('created_date', 'title')
