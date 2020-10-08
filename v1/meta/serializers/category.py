# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = 'pk', 'title'
        model = Category
