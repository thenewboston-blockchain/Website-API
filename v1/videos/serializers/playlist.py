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
        videos = validated_data.pop('videos', [])
        instance = super(PlaylistSerializer, self).update(instance, validated_data)

        for video in videos:
            pc, created = Video.objects.get_or_create(defaults={
                'video_id': video['video_id'],
                'title': video['title'],
                'description': video['description'],
                'duration': video['duration'],
                'thumbnail': video['thumbnail'],
                'language': video['language'],
                'video_type': video['video_type'],
                'author': video['author'],
                'category': video['category']

            }, playlist=instance)
            if not created:
                pc.video_id = video['video_id']
                pc.title = video['title']
                pc.description = video['description']
                pc.thumbnail = video['thumbnail']
                pc.language = video['language']
                pc.video_type = video['video_type']
                pc.author = video['author']
                pc.duration = video['duration']
                pc.category = ['category']
            pc.save()

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
