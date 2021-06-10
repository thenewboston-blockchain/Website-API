from rest_framework.serializers import ModelSerializer

from ..models.instagram import Instagram


class InstagramSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'account_reached', 'impressions', 'profile_visits', 'website_taps',
                  'content_interactions', 'followers', 'week_ending', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date',)
        model = Instagram
