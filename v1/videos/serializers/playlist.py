from django.db import transaction
from django.utils import dateparse
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


from .video import VideoSerializer
from ..models.playlist import Playlist
from ..models.video import Video


class PlaylistSerializer(ModelSerializer):
    video_list = VideoSerializer(
        source='videos',
        allow_null=True,
        many=True,
        required=False
    )

    class Meta:
        fields = '__all__'
        model = Playlist
        read_only_fields = 'published_at', 'created_date', 'modified_date'

    @transaction.atomic
    def create(self, validated_data):
        videos = validated_data.pop('videos', [])
        instance = super(PlaylistSerializer, self).create(validated_data)

        for video in videos:
            Video.objects.create(**video,
                                 playlist=instance
                                 )
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        videos_data = validated_data.pop('videos', [])
        videos = (instance.videos).all()
        videos = list(videos)
        instance.playlist_id = validated_data.get('playlist_id', instance.playlist_id)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)
        instance.language = validated_data.get('language', instance.language)
        instance.playlist_type = validated_data.get('playlist_type', instance.playlist_type)
        instance.author = validated_data.get('author', instance.author)
        instance.save()

        for video_data in videos_data:
            video = videos.pop(0)
            video.video_id = video_data.get('video_id', video.video_id)
            video.title = video_data.get('title', video.title)
            video.description = video_data.get('description', video.description)
            video.thumbnail = video_data.get('thumbnail', video.thumbnail)
            video.language = video_data.get('language', video.language)
            video.video_type = video_data.get('video_type', video.video_type)
            video.author = video_data.get('author', video.author)
            video.duration = video_data.get('duration', video.duration)
            video.category = video_data.get('category', video.category)
            video.tags = video_data.get('tags', video.tags)
            video.save()
        return instance

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
