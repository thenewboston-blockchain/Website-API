from django.utils import dateparse
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models.playlist import Playlist


class PlaylistSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Playlist
        read_only_fields = 'published_at', 'created_date', 'modified_date'

    def validate(self, data):
        published_at = self.context.get('request').data.get('published_at')
        published_at = dateparse.parse_datetime(published_at)
        if not published_at:
            raise serializers.ValidationError(
                {'published_at': 'Invalid datetime format'})
        else:
            data['published_at'] = published_at
        return data
