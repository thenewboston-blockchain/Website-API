# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Opening


class OpeningSerializer(serializers.ModelSerializer):

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
