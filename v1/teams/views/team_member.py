from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from ..models.team_member import CoreMember, TeamMember
from ..serializers.team import CoreMemberSerializer, TeamMemberSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class TeamMemberViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    filterset_fields = ['user']
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsStaffOrReadOnly]


class CoreMemberViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    filterset_fields = ['user']
    queryset = CoreMember.objects.all()
    serializer_class = CoreMemberSerializer
    permission_classes = [IsStaffOrReadOnly]
