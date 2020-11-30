# -*- coding: utf-8 -*-
from rest_framework import serializers

from v1.users.models.user import User
from ..models.product import Product
from ..models.product_image import ProductImage


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'image',
            'position',
        )
        model = ProductImage
        read_only_fields = 'created_date', 'modified_date'


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    product_images_meta = ProductImageSerializer(
        source='product_images',
        allow_null=True,
        many=True,
        required=False
    )

    class Meta:
        fields = (
            'user',
            'created_date',
            'modified_date',
            'pk',
            'description',
            'price',
            'published_at',
            'status',
            'title',
            'product_images_meta'
        )
        model = Product
        read_only_fields = 'created_date', 'modified_date'
