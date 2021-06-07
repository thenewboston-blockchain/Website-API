from rest_framework.serializers import ModelSerializer

from ..models.other_social import OtherSocial


class OtherSocialSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'discord_members', 'reddit_subscribers', 'youtube_subscribers',
                  'week_ending', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date', )
        model = OtherSocial
