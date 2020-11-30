# -*- coding: utf-8 -*-
from rest_framework import viewsets

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.product import Product
from ..serializers.product import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects \
        .prefetch_related('product_images') \
        .order_by('created_date') \
        .all()
    serializer_class = ProductSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
