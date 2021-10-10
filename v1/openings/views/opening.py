from django.db.models import Prefetch

from config.helpers.cache import CachedModelViewSet
from v1.teams.models.team_member import TeamMember
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.opening import Opening
from ..serializers.opening import OpeningSerializer, OpeningSerializerCreate


class OpeningViewSet(CachedModelViewSet):
    queryset = Opening.objects \
        .prefetch_related(Prefetch('team__team_members',
                                   queryset=TeamMember.objects.filter(is_lead=True)),
                          'responsibilities', 'skills') \
        .all()

    serializer_class = OpeningSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return OpeningSerializer
        if self.action in ['create', 'partial_update', 'update']:
            return OpeningSerializerCreate
        return OpeningSerializer
