from rest_framework import serializers

from ..models.skill import Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'pk', 'title', 'created_date', 'modified_date'
        model = Skill
        read_only_fields = 'created_date', 'modified_date'
