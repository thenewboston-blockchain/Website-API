# -*- coding: utf-8 -*-
from rest_framework import serializers

from ..models import Skill


class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        fields = 'pk', 'title'
        model = Skill
