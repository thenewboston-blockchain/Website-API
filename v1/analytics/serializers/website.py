from rest_framework.serializers import ModelSerializer

from ..models.website import Website


class WebsiteSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'users', 'sessions', 'bounce_rate', 'session_duration',
                  'week_ending', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date', )
        model = Website
