import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class LinkedIn(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    views = models.PositiveIntegerField()
    unique_visitors = models.PositiveIntegerField()
    custom_button_clicks = models.PositiveIntegerField()
    reactions = models.PositiveIntegerField()
    comments = models.PositiveIntegerField()
    shares = models.PositiveIntegerField()
    page_follow = models.PositiveIntegerField()
    week_ending = models.DateTimeField()

    class Meta:
        ordering = ('week_ending',)
        verbose_name_plural = 'linkedin'

    def __str__(self):
        return f'#{self.pk}: {self.week_ending}'
