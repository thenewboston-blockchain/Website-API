# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer

from ..models.repository import Repository


class RepositorySerializer(ModelSerializer):

    class Meta:
        fields = (
            'url',
            'display_name',
            'modified_date',
            'pk',
        )
        model = Repository

        read_only_fields = (
            'created_date',
            'modified_date'
        )
