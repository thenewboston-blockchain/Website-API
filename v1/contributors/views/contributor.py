# -*- coding: utf-8 -*-
from rest_framework import viewsets

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models import Contributor
from ..serializers import ContributorSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects \
        .order_by('created_date') \
        .all()
    serializer_class = ContributorSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
