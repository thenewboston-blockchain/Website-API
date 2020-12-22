# -*- coding: utf-8 -*-
from rest_framework.viewsets import ModelViewSet

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.repository import Repository
from ..serializers.repository import RepositorySerializer


class RepositoryViewSet(ModelViewSet):
    queryset = Repository.objects.order_by('created_date').all()
    serializer_class = RepositorySerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
