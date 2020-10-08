# -*- coding: utf-8 -*-
from rest_framework import mixins, viewsets

from ..models import Category
from ..serializers import CategorySerializer


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
