from rest_framework import serializers

from ..models.project import Project
from ..serializers.milestone import MilestoneSerializer


class ProjectSerializer(serializers.ModelSerializer):
    milestones = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Project
        read_only_fields = 'created_date', 'modified_date'

    def get_milestones(self, project):
        return MilestoneSerializer(project.milestone_set.all(), many=True).data
