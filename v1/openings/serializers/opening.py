# -*- coding: utf-8 -*-
from rest_framework import serializers

from v1.contributors.serializers import ContributorSerializer
from ..models import Opening


class OpeningSerializer(serializers.ModelSerializer):
    reports_to = ContributorSerializer(many=True)

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


class OpeningSerializerWrite(serializers.ModelSerializer):

    class Meta:
        fields = (
            'active',
            'description',
            'eligible_for_task_points',
            'pay_per_day',
            'reports_to',
            'responsibilities',
            'skills',
            'team',
            'title',
        )
        model = Opening
