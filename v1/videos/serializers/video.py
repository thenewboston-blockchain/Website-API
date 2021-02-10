from rest_framework.serializers import ModelSerializer

from ..models.video import Video


class VideoSerializer(ModelSerializer):
    class Meta:
        fields = ('pk', 'video_id', 'title', 'description', 'published_at',
                  'duration', 'author', 'tags', 'category', 'thumbnail',
                  'language', 'video_type', 'created_date', 'modified_date')
        model = Video
        read_only_fields = 'published_at', 'created_date', 'modified_date'
