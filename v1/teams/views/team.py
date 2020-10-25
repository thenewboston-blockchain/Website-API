# -*- coding: utf-8 -*-
from rest_framework import viewsets

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.team import Team
from ..serializers.team import TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects \
        .prefetch_related('team_members') \
        .order_by('created_date') \
        .all()
    serializer_class = TeamSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
