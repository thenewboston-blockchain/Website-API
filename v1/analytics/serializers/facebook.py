from rest_framework.serializers import ModelSerializer

from ..models.facebook import Facebook


class FacebookSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'actions_on_page', 'page_views', 'page_likes', 'post_reach', 'story_reach', 'recommendations', 'post_engagement',
                  'responsiveness', 'videos', 'followers', 'week_ending', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date',)
        model = Facebook
