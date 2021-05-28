from rest_framework.serializers import ModelSerializer

from ..models.playlist_category import PlaylistCategory


class PlaylistCategorySerializer(ModelSerializer):
    class Meta:
        fields = (
            'created_date',
            'modified_date',
            'name',
            'pk',
        )
        model = PlaylistCategory
        read_only_fields = 'created_date', 'modified_date'
