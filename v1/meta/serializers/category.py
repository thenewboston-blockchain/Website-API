# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = 'pk', 'title', 'created_date', 'modified_date'
        model = Category
        read_only_fields = 'created_date', 'modified_date'
