import uuid

from django.core.cache import cache
from django.db.models import CASCADE, CharField, ForeignKey, URLField, UUIDField
from thenewboston.models.created_modified import CreatedModified

from v1.teams.models.team import Team


class Repository(CreatedModified):
    uuid = UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    url = URLField(blank=True)
    display_name = CharField(max_length=80, unique=True)  # TNB-python-client
    team = ForeignKey(Team, on_delete=CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'repositories'

    def __str__(self):
        return f'#{self.pk}: {self.url} ({self.display_name})'

    def save(self, *args, **kwargs):
        cache.delete_pattern('views.decorators.cache.cache*')
        return super(Repository, self).save(*args, **kwargs)
