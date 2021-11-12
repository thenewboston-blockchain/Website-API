from django.db.models import Prefetch

from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly, IsSuperUserOrReadOnly, IsSuperUserOrTeamLead, ReadOnly
from ..models.team import CoreTeam, ProjectTeam, Team
from ..serializers.team import CoreTeamSerializer, ProjectTeamSerializer, TeamSerializer


class TeamViewSet(CachedModelViewSet):
    queryset = Team.objects \
        .prefetch_related(Prefetch('team_members')) \
        .order_by('created_date') \
        .all()
    serializer_class = TeamSerializer
    permission_classes = [IsStaffOrReadOnly]


class CoreTeamViewSet(CachedModelViewSet):
    queryset = CoreTeam.objects \
        .prefetch_related(Prefetch('core_members')) \
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


class ProjectTeamViewSet(CachedModelViewSet):
    queryset = ProjectTeam.objects \
        .prefetch_related('project_members') \
        .prefetch_related(Prefetch('project_members')) \
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
