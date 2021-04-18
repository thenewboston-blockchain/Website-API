import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Project(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=250)
    project_lead = models.ForeignKey('teams.ProjectMember', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    logo = models.URLField()
    github_url = models.URLField()
    overview = models.TextField()
    problem = models.TextField()
    target_market = models.TextField()
    benefits = models.TextField()
    centered_around_tnb = models.CharField(max_length=250)
    estimated_completion_date = models.DateTimeField()

    def __str__(self):
        return f'#{self.pk}: {self.title}'

    class Meta:
        ordering = ('created_date', 'title')
