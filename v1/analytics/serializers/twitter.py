from rest_framework.serializers import ModelSerializer

from ..models.twitter import Twitter


class TwitterSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'tweets', 'tweet_impressions', 'profile_visits', 'mentions', 'total_followers',
                  'new_followers', 'week_ending', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date', )
        model = Twitter
