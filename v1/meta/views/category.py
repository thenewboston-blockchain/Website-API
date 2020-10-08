# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import Category
from ..serializers import CategorySerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
