from rest_framework import serializers

from ..models.roadmap import Roadmap


class RoadmapSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.title', required=False, read_only=True)

    class Meta:
        fields = ('pk', 'team', 'team_name', 'task_title', 'estimated_completion_date', 'is_complete',\
                  'created_date', 'modified_date')
        model = Roadmap
        read_only_fields = ('created_date', 'modified_date', 'team_name', )
