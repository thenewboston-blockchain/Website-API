# -*- coding: utf-8 -*-
from django.db import transaction
from rest_framework import serializers

from ..models.team import Team
from ..models.team_member import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'created_date',
            'is_lead',
            'job_title',
            'modified_date',
            'pay_per_day',
            'team',
            'user',
        )
        model = TeamMember
        read_only_fields = 'created_date', 'modified_date', 'team'


class TeamSerializer(serializers.ModelSerializer):
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
            'title'
        )
        model = Team
        read_only_fields = 'created_date', 'modified_date'

    @transaction.atomic
    def create(self, validated_data):
        team_members = validated_data.pop('team_members', [])
        instance = super(TeamSerializer, self).create(validated_data)

        for team_member in team_members:
            TeamMember.objects.create(
                user=team_member['user'],
                is_lead=team_member['is_lead'],
                job_title=team_member['job_title'],
                pay_per_day=team_member['pay_per_day'],
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
                'pay_per_day': team_member['pay_per_day'],
                'job_title': team_member['job_title'],
            }, team=instance, user=team_member['user'])

            if not created:
                tc.is_lead = team_member['is_lead']
                tc.pay_per_day = team_member['pay_per_day']
                tc.job_title = team_member['job_title']
                tc.save()

        return instance
