from django.db import models

from .team import Team


class CoreTeam(Team):
    responsibilities = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'#{self.pk}: {self.title}'
