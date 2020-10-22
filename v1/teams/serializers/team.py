# -*- coding: utf-8 -*-
from django.db import transaction
from rest_framework import serializers

from ..models import Team, TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'user',
            'created_date',
            'is_lead',
            'modified_date',
            'pay_per_day',
        )
        model = TeamMember
        read_only_fields = 'created_date', 'modified_date'


class TeamSerializer(serializers.ModelSerializer):
    team_members_meta = TeamMemberSerializer(
        source='teammember_set',
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
        teammember_set = validated_data.pop('teammember_set', [])
        instance = super(TeamSerializer, self).create(validated_data)

        for teammember in teammember_set:
            TeamMember.objects.create(
                user=teammember['user'],
                is_lead=teammember['is_lead'],
                pay_per_day=teammember['pay_per_day'],
                team=instance
            )

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        teammember_set = validated_data.pop('teammember_set', [])
        instance = super(TeamSerializer, self).update(instance, validated_data)

        TeamMember.objects \
            .filter(team=instance) \
            .exclude(user__in=[teammember['user'].pk for teammember in teammember_set]) \
            .delete()

        for teammember in teammember_set:
            tc, created = TeamMember.objects.get_or_create(defaults={
                'is_lead': teammember['is_lead'],
                'pay_per_day': teammember['pay_per_day']
            }, team=instance, user=teammember['user'])

            if not created:
                tc.is_lead = teammember['is_lead']
                tc.pay_per_day = teammember['pay_per_day']
                tc.save()

        return instance
