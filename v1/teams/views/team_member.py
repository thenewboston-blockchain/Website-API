from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from ..models.team_member import TeamMember
from ..serializers.team import TeamMemberSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    filterset_fields = ['user']
    queryset = TeamMember.objects.select_related('team')
    serializer_class = TeamMemberSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]
