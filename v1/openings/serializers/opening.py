# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models.opening import Opening
from ...meta.models import Category, Responsibility, Skill
from ...teams.models import Contributor


class OpeningSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    responsibilities = serializers.PrimaryKeyRelatedField(many=True, queryset=Responsibility.objects.all())
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())

    reports_to = serializers.PrimaryKeyRelatedField(many=True, queryset=Contributor.objects.all())

    class Meta:
        fields = 'pk', 'title', 'description', 'pay_per_day', 'eligible_for_task_points', 'active', \
                 'reports_to', \
                 'categories', 'responsibilities', 'skills', \
                 'created_date', 'modified_date'
        model = Opening
        read_only_fields = 'created_date', 'modified_date'
