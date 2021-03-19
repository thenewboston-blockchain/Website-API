from rest_framework.viewsets import ModelViewSet

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly, IsSuperUserOrReadOnly, IsSuperUserOrTeamLead, ReadOnly
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
        .prefetch_related('core_members') \
        .order_by('created_date') \
        .all()
    serializer_class = CoreTeamSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'create']:
            permission_classes = [IsSuperUserOrReadOnly]
        elif self.action in ['partial_update', 'update']:
            permission_classes = [IsSuperUserOrTeamLead]
        else:
            permission_classes = [ReadOnly]

        return [permission() for permission in permission_classes]


class ProjectTeamViewSet(ModelViewSet):
    queryset = ProjectTeam.objects \
        .prefetch_related('project_members') \
        .order_by('created_date') \
        .all()
    serializer_class = ProjectTeamSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'create']:
            permission_classes = [IsSuperUserOrReadOnly]
        elif self.action in ['partial_update', 'update']:
            permission_classes = [IsSuperUserOrTeamLead]
        else:
            permission_classes = [ReadOnly]

        return [permission() for permission in permission_classes]
