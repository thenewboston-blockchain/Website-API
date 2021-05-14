from rest_framework.serializers import ModelSerializer

from ..models.category import PlaylistCategory


class PlaylistCategorySerializer(ModelSerializer):
    class Meta:
        fields = ('pk', 'name', 'created_date',
                  'modified_date',)
        model = PlaylistCategory
        read_only_fields = 'created_date', 'modified_date'
