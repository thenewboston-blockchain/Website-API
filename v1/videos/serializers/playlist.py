from django.db import transaction
from django.utils import dateparse
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .video import VideoSerializer
from ..models.instructor import Instructor
from ..models.playlist import Playlist
from ..models.video import Video
from ..serializers.instructor import InstructorSerializer


class PlaylistSerializerCreate(ModelSerializer):
    video_list = VideoSerializer(
        source='videos',
        allow_null=True,
        many=True,
        required=False
    )
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all())
    duration = serializers.SerializerMethodField('total_duration')

    class Meta:
        fields = ('pk', 'title', 'description', 'published_at', 'instructor',
                  'thumbnail', 'categories', 'playlist_type', 'video_list', 'duration', 'is_featured', 'created_date', 'modified_date',)
        model = Playlist
        read_only_fields = 'created_date', 'modified_date'

    @transaction.atomic
    def create(self, validated_data):
        videos = validated_data.pop('videos', [])
        instance = super(PlaylistSerializerCreate, self).create(validated_data)

        for video in videos:
            Video.objects.create(**video, playlist=instance)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        videos_data = validated_data.pop('videos', [])
        videos = (instance.videos).all()
        videos = list(videos)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.thumbnail = validated_data.get('thumbnail', instance.thumbnail)
        instance.playlist_type = validated_data.get('playlist_type', instance.playlist_type)
        categories = validated_data.get('categories', [])
        for category in categories:
            instance.categories.add(category)
        instance.save()

        for video_data in videos_data:
            video = videos.pop(0)
            video.video_id = video_data.get('video_id', video.video_id)
            video.title = video_data.get('title', video.title)
            video.description = video_data.get('description', video.description)
            video.thumbnail = video_data.get('thumbnail', video.thumbnail)
            video.duration_seconds = video_data.get('duration_seconds', video.duration_seconds)
            video.position = video_data.get('position', video.position)
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

    def total_duration(self, obj):
        videos = obj.videos.all()
        total = 0
        for video in videos:
            total += video.duration_seconds
        return total


class PlaylistSerializer(ModelSerializer):
    video_list = VideoSerializer(
        source='videos',
        allow_null=True,
        many=True,
        required=False
    )
    instructor = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField('total_duration')

    class Meta:
        fields = ('pk', 'title', 'description', 'published_at', 'instructor',
                  'thumbnail', 'categories', 'playlist_type', 'video_list', 'duration', 'is_featured', 'created_date', 'modified_date',)
        model = Playlist
        read_only_fields = 'created_date', 'modified_date'

    def to_representation(self, obj):
        # get the original representation
        playlist = super(PlaylistSerializer, self).to_representation(obj)
        include_videos = self.context.get('request').query_params.get('include_videos')
        if include_videos:
            if include_videos not in ['True', 'False', 'true', 'false']:
                raise serializers.ValidationError({'detail': 'Please provide a boolean value: True,False/true,false'})
            if include_videos in ['False', 'false']:
                playlist.pop('video_list')
        return playlist

    def get_instructor(self, playlist):
        return InstructorSerializer(playlist.instructor).data

    def total_duration(self, obj):
        videos = obj.videos.all()
        total = 0
        for video in videos:
            total += video.duration_seconds
        return total
