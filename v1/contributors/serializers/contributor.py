# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Contributor


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'account_number',
            'created_date',
            'display_name',
            'github_username',
            'modified_date',
            'pk',
            'profile_image',
            'slack_username',
        )
        model = Contributor
        read_only_fields = 'created_date', 'modified_date', 'profile_image'
