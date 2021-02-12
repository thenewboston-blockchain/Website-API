from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from ..models.team_member import TeamMember
from ..serializers.team import TeamMemberSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class TeamMemberViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    filterset_fields = ['user']
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    # pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
