from rest_framework.serializers import ModelSerializer

from ..models.community import Community


class CommunitySerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'projects_approved', 'projects_completed', 'week_ending', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date', )
        model = Community
