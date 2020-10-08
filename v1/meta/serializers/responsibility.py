# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Responsibility


class ResponsibilitySerializer(serializers.ModelSerializer):

    class Meta:
        fields = 'pk', 'title'
        model = Responsibility
