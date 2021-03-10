import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Team(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=250)
    about = models.TextField(default='')
    github = models.URLField(blank=True, null=True)
    slack = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f'#{self.pk}: {self.title}'

    class Meta:
        ordering = ('created_date', 'title')


class CoreTeam(Team):
    responsibilities = models.TextField(blank=True, null=True)


class ProjectTeam(Team):
    external_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
