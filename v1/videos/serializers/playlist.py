from rest_framework.serializers import ModelSerializer

from ..models.playlist import Playlist


class PlaylistSerializer(ModelSerializer):
    class Meta:
        fields = ('pk', 'playlist_id', 'items', 'title', 'description', 'published_at',
                  'author', 'thumbnail', 'language', 'playlist_type',
                  'created_date', 'modified_date')
        model = Playlist
        read_only_fields = 'published_at', 'created_date', 'modified_date'
