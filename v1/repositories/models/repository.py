import uuid

from django.db.models import CharField, DO_NOTHING, ForeignKey, URLField, UUIDField
from thenewboston.models.created_modified import CreatedModified

from v1.teams.models.team import Team


class Repository(CreatedModified):
    uuid = UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    url = URLField(blank=True)
    display_name = CharField(max_length=80, unique=True)  # TNB-python-client
    team = ForeignKey(Team, on_delete=DO_NOTHING)

    class Meta:
        verbose_name_plural = 'repositories'

    def __str__(self):
        return f'#{self.pk}: {self.url} ({self.display_name})'
