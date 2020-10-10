# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import Team
from ..serializers import TeamSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects \
        .prefetch_related('teamcontributor_set') \
        .order_by('created_date') \
        .all()
    serializer_class = TeamSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
