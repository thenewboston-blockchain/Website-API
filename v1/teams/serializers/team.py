from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

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
            'pk'
        )
        model = TeamMember
        read_only_fields = 'created_date', 'modified_date', 'team'


class CoreMemberSerializer(TeamMemberSerializer):

    class Meta(TeamMemberSerializer.Meta):
        fields = TeamMemberSerializer.Meta.fields + ('core_team', 'pay_per_day',)
        model = CoreMember
        read_only_fields = TeamMemberSerializer.Meta.read_only_fields + ('core_team',)

    def create(self, validated_data):
        try:
            core_team_id = self.context.get('request').data.get('core_team')
            if not core_team_id:
                raise serializers.ValidationError({'core_team': ['This field is required.']})
            core_team = CoreTeam.objects.get(pk=core_team_id)
            validated_data['core_team'] = core_team
            return super().create(validated_data)
        except CoreTeam.DoesNotExist:
            raise serializers.ValidationError({'core_team': ['CoreTeam not found', ]})
        except ValidationError:
            raise serializers.ValidationError({'core_team': ['{} is not a valid UUID.'.format(core_team_id), ]})


class ProjectMemberSerializer(TeamMemberSerializer):
    class Meta:
        fields = TeamMemberSerializer.Meta.fields + ('project_team',)
        model = ProjectMember
        read_only_fields = TeamMemberSerializer.Meta.read_only_fields + ('project_team',)

    def create(self, validated_data):
        try:
            project_team_id = self.context.get('request').data.get('project_team')
            if not project_team_id:
                raise serializers.ValidationError({'project_team': ['This field is required.']})
            project_team = ProjectTeam.objects.get(pk=project_team_id)
            validated_data['project_team'] = project_team
            return super().create(validated_data)
        except ProjectTeam.DoesNotExist:
            raise serializers.ValidationError({'project_team': ['ProjectTeam not found', ]})
        except ValidationError:
            raise serializers.ValidationError({'project_team': ['{} is not a valid UUID.'.format(project_team_id), ]})


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
    core_members_meta = CoreMemberSerializer(
        source='core_members',
        allow_null=True,
        many=True,
        required=False
    )

    class Meta:
        fields = TeamSerializer.Meta.fields + ('core_members_meta', 'responsibilities',)
        model = CoreTeam

    @transaction.atomic
    def create(self, validated_data):
        core_members = validated_data.pop('core_members', [])
        instance = super(CoreTeamSerializer, self).create(validated_data)

        for core_member in core_members:
            CoreMember.objects.create(**core_member,
                                      core_team=instance
                                      )
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        core_members = validated_data.pop('core_members', [])
        instance = super(CoreTeamSerializer, self).update(instance, validated_data)

        CoreMember.objects \
            .filter(core_team=instance) \
            .exclude(user__in=[core_member['user'].pk for core_member in core_members]) \
            .delete()

        for core_member in core_members:
            tc, created = CoreMember.objects.get_or_create(defaults={
                'is_lead': core_member.get('is_lead'),
                'job_title': core_member.get('job_title', ''),
                'pay_per_day': core_member.get('pay_per_day', 2800)
            }, core_team=instance, user=core_member['user'])

            if not created:
                tc.is_lead = core_member.get('is_lead', tc.is_lead)
                tc.job_title = core_member.get('job_title', tc.job_title)
                tc.pay_per_day = core_member.get('pay_per_day', tc.pay_per_day)
                tc.save()

        return instance


class ProjectTeamSerializer(TeamSerializer):
    project_members_meta = ProjectMemberSerializer(
        source='project_members',
        allow_null=True,
        many=True,
        required=False
    )

    class Meta:
        fields = TeamSerializer.Meta.fields + ('project_members_meta', 'is_active', 'external_url',)
        model = ProjectTeam

    @ transaction.atomic
    def create(self, validated_data):
        project_members = validated_data.pop('project_members', [])
        instance = super(ProjectTeamSerializer, self).create(validated_data)

        for project_member in project_members:
            ProjectMember.objects.create(**project_member,
                                         project_team=instance
                                         )
        return instance

    @ transaction.atomic
    def update(self, instance, validated_data):
        project_members = validated_data.pop('project_members', [])
        instance = super(ProjectTeamSerializer, self).update(instance, validated_data)

        ProjectMember.objects \
            .filter(project_team=instance) \
            .exclude(user__in=[project_member['user'].pk for project_member in project_members])\
            .delete()

        for project_member in project_members:
            tc, created = ProjectMember.objects.get_or_create(defaults={
                'is_lead': project_member.get('is_lead'),
                'job_title': project_member.get('job_title', ''),
            }, project_team=instance, user=project_member['user'])

            if not created:
                tc.is_lead = project_member.get('is_lead', tc.is_lead)
                tc.job_title = project_member.get('job_title', tc.job_title)
                tc.save()

        return instance
