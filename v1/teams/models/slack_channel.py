import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified

from v1.teams.models.team import Team

class SlackChannel(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name  = models.CharField(max_length=250)
    team  = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'#{self.pk}: {self.title}'

    class Meta:
        ordering = ('created_date', 'name')
