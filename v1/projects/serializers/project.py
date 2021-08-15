from rest_framework import serializers

from ..models.project import Project
from ..serializers.milestone import MilestoneSerializer


class ProjectSerializer(serializers.ModelSerializer):
    milestones = serializers.SerializerMethodField()
    project_lead_display_name = serializers.CharField(source='project_lead.user.display_name', required=False)

    class Meta:
        fields = (
            'benefits',
            'centered_around_tnb',
            'created_date',
            'description',
            'estimated_completion_date',
            'github_url',
            'logo',
            'milestones',
            'modified_date',
            'overview',
            'pk',
            'problem',
            'project_lead',
            'project_lead_display_name',
            'target_market',
            'title',
            'is_featured'
        )
        model = Project
        read_only_fields = 'created_date', 'modified_date', 'project_lead_display_name'

    def get_milestones(self, project):
        return MilestoneSerializer(project.milestone_set.all(), many=True).data
