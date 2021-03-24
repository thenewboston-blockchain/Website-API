import uuid

from django.db import models
from rest_framework import serializers
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
    hourly_rate = models.PositiveIntegerField()
    weekly_hourly_commitment = models.PositiveIntegerField(default=0)
    core_team = models.ForeignKey('teams.CoreTeam', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'core_members'

    def validate_unique(self, exclude=None):
        q = CoreMember.objects.filter(user=self.user, core_team=self.core_team)
        if self.pk is None:
            if q.filter(user=self.user).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'CoreMember with {} and {} already exists.'.format(self.user, self.core_team),
                    }
                )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.validate_unique()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class ProjectMember(TeamMember):
    project_team = models.ForeignKey('teams.ProjectTeam', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'project_members'

    def validate_unique(self, exclude=None):
        q = ProjectMember.objects.filter(user=self.user, project_team=self.project_team)
        if self.pk is None:
            if q.filter(user=self.user).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'ProjectMember with {} and {} already exists.'.format(self.user, self.project_team),
                    }
                )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.validate_unique()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
