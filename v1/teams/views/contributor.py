# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import Contributor
from ..serializers import ContributorSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects \
        .order_by('created_date') \
        .all()
    serializer_class = ContributorSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
