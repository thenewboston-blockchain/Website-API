from django.db import models

from .team import Team


class ProjectTeam(Team):
    external_url = models.URLField(blank=True, null=True, max_length=500)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'#{self.pk}: {self.title}'
