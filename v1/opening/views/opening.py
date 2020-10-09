# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import Opening
from ..serializers import OpeningSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class OpeningViewSet(viewsets.ModelViewSet):
    queryset = Opening.objects \
        .prefetch_related('categories', 'responsibilities', 'skills') \
        .order_by('created_date') \
        .all()
    serializer_class = OpeningSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
