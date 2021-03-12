from django.db import transaction
from rest_framework import serializers

from ..models.slack_channel import SlackChannel
from ..models.team import CoreTeam, ProjectTeam, Team
from ..models.team_member import CoreMember, ProjectMember, TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'created_date',
            'is_lead',
            'job_title',
            'modified_date',
            'team',
            'user',
        )
        model = TeamMember
        read_only_fields = 'created_date', 'modified_date', 'team'


class TeamSerializer(serializers.ModelSerializer):
    about = serializers.CharField(required=True)
    team_members_meta = TeamMemberSerializer(
        source='team_members',
        allow_null=True,
        many=True,
        required=False
    )

    class Meta:
        fields = (
            'team_members_meta',
            'created_date',
            'modified_date',
            'pk',
            'title',
            'about',
            'github',
            'slack'
        )
        model = Team
        read_only_fields = 'created_date', 'modified_date',

    @transaction.atomic
    def create(self, validated_data):
        team_members = validated_data.pop('team_members', [])
        instance = super(TeamSerializer, self).create(validated_data)

        for team_member in team_members:
            TeamMember.objects.create(
                user=team_member['user'],
                is_lead=team_member['is_lead'],
                job_title=team_member['job_title'],
                team=instance
            )

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        team_members = validated_data.pop('team_members', [])
        instance = super(TeamSerializer, self).update(instance, validated_data)

        TeamMember.objects \
            .filter(team=instance) \
            .exclude(user__in=[team_member['user'].pk for team_member in team_members]) \
            .delete()

        for team_member in team_members:
            tc, created = TeamMember.objects.get_or_create(defaults={
                'is_lead': team_member['is_lead'],
                'job_title': team_member['job_title'],
            }, team=instance, user=team_member['user'])

            if not created:
                tc.is_lead = team_member['is_lead']
                tc.job_title = team_member['job_title']
                tc.save()

        return instance


class CoreTeamSerializer(TeamSerializer):
    class Meta:
        fields = TeamSerializer.Meta.fields + ('responsibilities',)
        model = CoreTeam


class ProjectTeamSerializer(TeamSerializer):
    class Meta:
        fields = TeamSerializer.Meta.fields + ('is_active', 'external_url',)
        model = ProjectTeam


class SlackChannelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'created_date',
            'name',
            'modified_date',
            'team',
            'pk'
        )
        model = SlackChannel
        read_only_fields = 'created_date', 'modified_date'


class CoreMemberSerializer(TeamMemberSerializer):
    class Meta:
        fields = TeamMemberSerializer.Meta.fields + ('core_team', 'pay_per_day',)
        model = CoreMember


class ProjectMemberSerializer(TeamMemberSerializer):
    class Meta:
        fields = TeamMemberSerializer.Meta.fields + ('project_team',)
        model = ProjectMember
