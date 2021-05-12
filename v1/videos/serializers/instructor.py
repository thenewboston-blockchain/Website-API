from rest_framework.serializers import ModelSerializer

from ..models.instructor import Instructor


class InstructorSerializer(ModelSerializer):
    class Meta:
        fields = ('pk', 'name', 'youtube_url', 'vimeo_url', 'created_date',
                  'modified_date',)
        model = Instructor
        read_only_fields = 'created_date', 'modified_date'
