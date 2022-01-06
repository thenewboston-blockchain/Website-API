from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from ..models.app import App, AppImage, Category


class AppSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'name', 'description', 'logo', 'website', 'images', 'tagline', 'category', 'slug', 'page_hits',
                  'created_date', 'modified_date')
        model = App
        lookup_field = 'slug'
        read_only_fields = ('created_date', 'modified_date',)
        depth = 1


class AppSerializerCreate(ModelSerializer):
    slug = serializers.CharField(
        validators=[UniqueValidator(queryset=App.objects.all())]
    )

    class Meta:
        fields = ('pk', 'name', 'description', 'logo', 'website', 'images', 'tagline', 'category', 'slug', 'page_hits',
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
