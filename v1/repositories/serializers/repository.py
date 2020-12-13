# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer

from ..models.repository import Repository


class RepositorySerializer(ModelSerializer):

    class Meta:
        fields = 'pk', 'url', 'display_name', 'created_date', 'modified_date'
        model = Repository
        read_only_fields = 'created_date', 'modified_date'
