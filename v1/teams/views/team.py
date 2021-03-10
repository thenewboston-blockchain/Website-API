from rest_framework.viewsets import ModelViewSet

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.team import CoreTeam, ProjectTeam, Team
from ..serializers.team import CoreTeamSerializer, ProjectTeamSerializer, TeamSerializer


class TeamViewSet(ModelViewSet):
    queryset = Team.objects \
        .prefetch_related('team_members') \
        .order_by('created_date') \
        .all()
    serializer_class = TeamSerializer
    permission_classes = [IsStaffOrReadOnly]


class CoreTeamViewSet(ModelViewSet):
    queryset = CoreTeam.objects \
        .prefetch_related('team_members') \
        .order_by('created_date') \
        .all()
    serializer_class = CoreTeamSerializer
    permission_classes = [IsStaffOrReadOnly]


class ProjectTeamViewSet(ModelViewSet):
    queryset = ProjectTeam.objects \
        .prefetch_related('team_members') \
        .order_by('created_date') \
        .all()
    serializer_class = ProjectTeamSerializer
    permission_classes = [IsStaffOrReadOnly]
