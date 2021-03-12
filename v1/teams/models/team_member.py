import uuid

from django.db import models
from thenewboston.models.created_modified import CreatedModified


class TeamMember(CreatedModified):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    team = models.ForeignKey('teams.Team', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_lead = models.BooleanField(default=False)
    job_title = models.CharField(max_length=250)

    class Meta:
        default_related_name = 'team_members'
        unique_together = (
            ('team', 'user'),
        )
        ordering = ('created_date', 'job_title')


class CoreMember(TeamMember):
    pay_per_day = models.PositiveIntegerField(default=2800)
    core_team = models.ForeignKey('teams.CoreTeam', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'core_members'


class ProjectMember(TeamMember):
    project_team = models.ForeignKey('teams.ProjectTeam', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'project_members'
