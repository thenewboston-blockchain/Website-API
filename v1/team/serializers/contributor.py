# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Contributor


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'pk', 'display_name', 'github_username', 'slack_username', \
                 'created_date', 'modified_date'
        model = Contributor
        read_only_fields = 'created_date', 'modified_date'
