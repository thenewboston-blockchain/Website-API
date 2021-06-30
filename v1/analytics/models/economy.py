import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Economy(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    total_coins_distributed = models.PositiveIntegerField()
    total_coins_distributed_to_core_team = models.PositiveIntegerField()
    total_coins_distributed_to_faucet = models.PositiveIntegerField()
    total_coins_distributed_to_projects = models.PositiveIntegerField()
    week_ending = models.DateTimeField()

    class Meta:
        ordering = ('week_ending',)
        verbose_name_plural = 'economy'

    def __str__(self):
        return f'#{self.pk}: {self.week_ending}'
