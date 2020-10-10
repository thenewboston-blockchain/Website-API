# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Task
from ...contributors.models import Contributor


class TaskSerializer(serializers.ModelSerializer):
    contributor = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all())

    class Meta:
        fields = (
            'amount',
            'completed_date',
            'contributor',
            'created_date',
            'modified_date',
            'pk',
            'repository',
            'title',
        )
        model = Task
        read_only_fields = 'created_date', 'modified_date'
