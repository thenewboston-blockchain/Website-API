import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class Facebook(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    actions_on_page = models.PositiveIntegerField()
    page_views = models.PositiveIntegerField()
    page_likes = models.PositiveIntegerField()
    post_reach = models.PositiveIntegerField()
    story_reach = models.PositiveIntegerField()
    recommendations = models.PositiveIntegerField()
    post_engagement = models.PositiveIntegerField()
    responsiveness = models.PositiveIntegerField()
    videos = models.PositiveIntegerField()
    followers = models.PositiveIntegerField()
    week_ending = models.DateTimeField()

    class Meta:
        ordering = ('week_ending',)
        verbose_name_plural = 'facebook'
