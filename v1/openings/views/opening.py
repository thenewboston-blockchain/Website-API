from django.db.models import Prefetch

from config.helpers.cache import CachedModelViewSet
from v1.teams.models.team_member import TeamMember
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.opening import Opening
from ..serializers.opening import OpeningSerializer


class OpeningViewSet(CachedModelViewSet):
    queryset = Opening.objects \
        .prefetch_related(Prefetch('team__team_members',
                                   queryset=TeamMember.objects.filter(is_lead=True)),
                          'responsibilities', 'skills') \
        .all()

    serializer_class = OpeningSerializer
    permission_classes = [IsStaffOrReadOnly]
