from django.core.exceptions import ValidationError
from rest_framework import serializers
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

    def create(self, data):
        try:

            category_id = self.context.get('request').data.get('category')
            if not category_id:
                raise serializers.ValidationError({'category': ['This field is required.']})
            category = Category.objects.get(pk=category_id)
            data['category'] = category
            return super().create(data)
        except Category.DoesNotExist:
            raise serializers.ValidationError({'category': ['Category not found', ]})
        except ValidationError:
            raise serializers.ValidationError({'category': ['{} is not a valid UUID.'.format(category_id), ]})


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
