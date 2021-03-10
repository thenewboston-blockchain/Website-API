from rest_framework.viewsets import ModelViewSet

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.core_team import CoreTeam
from ..serializers.team import CoreTeamSerializer


class CoreTeamViewSet(ModelViewSet):
    queryset = CoreTeam.objects \
        .prefetch_related('team_members') \
        .order_by('created_date') \
        .all()
    serializer_class = CoreTeamSerializer
    permission_classes = [IsStaffOrReadOnly]
