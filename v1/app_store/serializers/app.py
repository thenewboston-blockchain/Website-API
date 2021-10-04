from rest_framework.serializers import ModelSerializer

from ..models.app import App, AppImage, Category


class AppSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'name', 'description', 'logo', 'website', 'images', 'tagline', 'category',
                  'created_date', 'modified_date')
        model = App
        read_only_fields = ('created_date', 'modified_date',)
        depth = 1


class AppSerializerCreate(ModelSerializer):

    class Meta:
        fields = ('pk', 'name', 'description', 'logo', 'website', 'images', 'tagline', 'category',
                  'created_date', 'modified_date')
        model = App
        read_only_fields = ('created_date', 'modified_date',)


class AppImageSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'app', 'image', 'created_date', 'modified_date')
        model = AppImage
        read_only_fields = ('created_date', 'modified_date',)


class CategorySerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'name', 'created_date', 'modified_date')
        model = Category
        read_only_fields = ('created_date', 'modified_date',)
