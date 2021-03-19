from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from ..models.team_member import CoreMember, ProjectMember, TeamMember
from ..serializers.team import CoreMemberSerializer, ProjectMemberSerializer, TeamMemberSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly, IsSuperUserOrReadOnly, IsSuperUserOrTeamLead, ReadOnly


class TeamMemberViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    filterset_fields = ['user']
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsStaffOrReadOnly]


class CoreMemberViewSet(ModelViewSet):
    filterset_fields = ['user']
    queryset = CoreMember.objects.all()
    serializer_class = CoreMemberSerializer

    def create(self, request, *args, **kwargs):
        try:
            member = CoreMember.objects.get(user=request.user, core_team=request.data.get('core_team'))
            is_lead = member.is_lead or request.user.is_superuser
        except CoreMember.DoesNotExist:
            is_lead = request.user.is_superuser
        if not is_lead:
            return Response({'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['destroy']:
            permission_classes = [IsSuperUserOrReadOnly]
        elif self.action in ['create', 'partial_update', 'update']:
            permission_classes = [IsSuperUserOrTeamLead]
        else:
            permission_classes = [ReadOnly]

        return [permission() for permission in permission_classes]


class ProjectMemberViewSet(ModelViewSet):
    filterset_fields = ['user']
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer

    def get_permissions(self):
        if self.action in ['destroy']:
            permission_classes = [IsSuperUserOrReadOnly]
        elif self.action in ['create', 'partial_update', 'update']:
            permission_classes = [IsSuperUserOrTeamLead]
        else:
            permission_classes = [ReadOnly]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            member = ProjectMember.objects.get(user=request.user, project_team=request.data.get('project_team'))
            is_lead = member.is_lead or request.user.is_superuser
        except ProjectMember.DoesNotExist:
            is_lead = request.user.is_superuser
        if not is_lead:
            return Response({'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)
