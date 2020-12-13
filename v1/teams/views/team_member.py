# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models.team_member import TeamMember
from ..serializers.team import TeamMemberSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class TeamMemberViewSet(viewsets.ModelViewSet):
    filterset_fields = ['user']
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
