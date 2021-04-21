from rest_framework import serializers

from ..models.project import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Project
        read_only_fields = 'created_date', 'modified_date'
