from rest_framework import serializers

from ..models.project import Project
from ..serializers.milestone import MilestoneSerializer


class ProjectSerializer(serializers.ModelSerializer):
    milestones = serializers.SerializerMethodField()

    class Meta:
        fields = ('pk', 'title', 'project_lead', 'description', 'logo', 'github_url',
                  'overview', 'problem', 'target_market', 'benefits', 'centered_around_tnb',
                  'estimated_completion_date', 'milestones', 'created_date', 'modified_date',)
        model = Project
        read_only_fields = 'created_date', 'modified_date'

    def get_milestones(self, project):
        return MilestoneSerializer(project.milestone_set.all(), many=True).data
