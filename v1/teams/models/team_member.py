import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class TeamMember(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    is_lead = models.BooleanField(default=False)
    job_title = models.CharField(max_length=250)

    class Meta:
        default_related_name = 'team_members'
        ordering = ('created_date', 'job_title')
