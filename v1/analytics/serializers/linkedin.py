from rest_framework.serializers import ModelSerializer

from ..models.linkedin import LinkedIn


class LinkedInSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'views', 'unique_visitors', 'custom_button_clicks', 'reactions', 'comments',
                  'shares', 'page_follow', 'week_ending', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date', )
        model = LinkedIn
