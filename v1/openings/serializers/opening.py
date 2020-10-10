# -*- coding: utf-8 -*-
from rest_framework import serializers

from v1.teams.models.team import Team
from ..models.opening import Opening
from ...contributors.models import Contributor
from ...meta.models import Responsibility, Skill


class OpeningSerializer(serializers.ModelSerializer):
    reports_to = serializers.PrimaryKeyRelatedField(many=True, queryset=Contributor.objects.all())
    responsibilities = serializers.PrimaryKeyRelatedField(many=True, queryset=Responsibility.objects.all())
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    class Meta:
        fields = (
            'active',
            'created_date',
            'description',
            'eligible_for_task_points',
            'modified_date',
            'pay_per_day',
            'pk',
            'reports_to',
            'responsibilities',
            'skills',
            'team',
            'title',
        )
        model = Opening
        read_only_fields = 'created_date', 'modified_date'
