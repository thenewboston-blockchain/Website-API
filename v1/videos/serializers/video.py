from django.core.exceptions import ValidationError
from django.utils import dateparse
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models.playlist import Playlist
from ..models.video import Video


class VideoSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Video
        read_only_fields = 'playlist', 'created_date', 'modified_date'

    def validate(self, data):
        published_at = self.context.get('request').data.get('published_at')
        if published_at:
            published_at = dateparse.parse_datetime(published_at)
            if not published_at:
                raise serializers.ValidationError(
                    {'published_at': 'Invalid datetime format'})
            else:
                data['published_at'] = published_at
        return data

    def create(self, data):
        try:
            playlist_id = self.context.get('request').data.get('playlist')
            if not playlist_id:
                raise serializers.ValidationError({'playlist': ['This field is required.']})
            playlist = Playlist.objects.get(pk=playlist_id)
            data['playlist'] = playlist
            return super().create(data)
        except Playlist.DoesNotExist:
            raise serializers.ValidationError({'playlist': ['Playlist not found', ]})
        except ValidationError:
            raise serializers.ValidationError({'playlist': ['{} is not a valid UUID.'.format(playlist_id), ]})
