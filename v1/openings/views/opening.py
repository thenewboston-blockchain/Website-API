from django.db.models import Prefetch
from rest_framework import viewsets

from v1.teams.models.team_member import TeamMember
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.opening import Opening
from ..serializers.opening import OpeningSerializer


class OpeningViewSet(viewsets.ModelViewSet):
    queryset = Opening.objects \
        .prefetch_related(Prefetch('team__team_members',
                                   queryset=TeamMember.objects.filter(is_lead=True)),
                          'responsibilities', 'skills') \
        .all()

    serializer_class = OpeningSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
