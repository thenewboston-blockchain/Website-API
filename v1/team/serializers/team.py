# -*- coding: utf-8 -*-
from django.db import transaction
from rest_framework import serializers

from ..models import Team, TeamContributor


class TeamContributorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'contributor', 'is_lead', 'pay_per_day', \
                 'created_date', 'modified_date'
        model = TeamContributor
        read_only_fields = 'created_date', 'modified_date'


class TeamSerializer(serializers.ModelSerializer):
    contributors_meta = TeamContributorSerializer(source='teamcontributor_set', many=True, allow_null=True, required=False)

    class Meta:
        fields = 'pk', 'title', 'contributors_meta', \
                 'created_date', 'modified_date'
        model = Team
        read_only_fields = 'created_date', 'modified_date'

    @transaction.atomic
    def create(self, validated_data):
        teamcontributor_set = validated_data.pop('teamcontributor_set', [])
        instance = super(TeamSerializer, self).create(validated_data)
        for teamcontributor in teamcontributor_set:
            TeamContributor.objects.create(contributor=teamcontributor['contributor'],
                                           is_lead=teamcontributor['is_lead'],
                                           pay_per_day=teamcontributor['pay_per_day'],
                                           team=instance)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        teamcontributor_set = validated_data.pop('teamcontributor_set', [])
        instance = super(TeamSerializer, self).update(instance, validated_data)

        TeamContributor.objects \
            .filter(team=instance) \
            .exclude(contributor__in=[teamcontributor['contributor'].pk for teamcontributor in teamcontributor_set]) \
            .delete()
        for teamcontributor in teamcontributor_set:
            tc, created = TeamContributor.objects.get_or_create(defaults={
                'is_lead': teamcontributor['is_lead'],
                'pay_per_day': teamcontributor['pay_per_day']
            }, team=instance, contributor=teamcontributor['contributor'])
            if not created:
                tc.is_lead = teamcontributor['is_lead']
                tc.pay_per_day = teamcontributor['pay_per_day']
                tc.save()
        return instance
