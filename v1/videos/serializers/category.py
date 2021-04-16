from rest_framework.serializers import ModelSerializer

from ..models.category import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ('pk', 'name', 'created_date',
                  'modified_date',)
        model = Category
        read_only_fields = 'created_date', 'modified_date'
