# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Task
from ...team.models import Contributor


class TaskSerializer(serializers.ModelSerializer):
    contributor = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all())

    class Meta:
        fields = 'pk', 'title', 'contributor', 'repository', 'completed_date', 'amount', \
                 'created_date', 'modified_date'
        model = Task
        read_only_fields = 'created_date', 'modified_date'

