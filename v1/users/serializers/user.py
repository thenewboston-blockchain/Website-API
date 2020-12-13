# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer

from ..models.user import User


class UserSerializer(ModelSerializer):

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
        model = User

        read_only_fields = (
            'created_date',
            'modified_date',
            'profile_image'
        )


class UpdateSelfUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = (
            'created_date',
            'github_username',
            'modified_date',
            'profile_image'
        )
