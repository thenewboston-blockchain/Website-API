from django.core.exceptions import ValidationError
from rest_framework import mixins, status
from rest_framework.response import Response

from config.helpers.cache import CachedGenericViewSet, CachedModelViewSet
from ..models.team_member import CoreMember, ProjectMember, TeamMember
from ..serializers.team import (
    CoreMemberSerializer,
    CoreMemberSerializerCreate,
    ProjectMemberSerializer,
    ProjectMemberSerializerCreate,
    TeamMemberSerializer
)
from ...third_party.rest_framework.permissions import (
    IsStaffOrReadOnly,
    IsSuperUserOrReadOnly,
    IsSuperUserOrTeamLead,
    ReadOnly
)


class TeamMemberViewSet(
    mixins.RetrieveModelMixin,
    CachedGenericViewSet
):
    filterset_fields = ['user']
    queryset = TeamMember.objects.select_related('user').order_by('created_date').all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request):  # noqa: ignore=A003
        user = request.query_params.get('user')
        if user:
            try:
                members = TeamMember.objects.filter(user=user).order_by('created_date')
                page = self.paginate_queryset(members)
            except ValidationError:
                return Response(
                    {'detail': f'{user} is not a valid UUID'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except TeamMember.DoesNotExist:
                return Response(
                    {'detail': f'No TeamMember with User ID: {user} was found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            page = self.paginate_queryset(self.queryset)
        serializer = self.serializer_class(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)


class CoreMemberViewSet(CachedModelViewSet):
    filterset_fields = ['user']
    queryset = CoreMember.objects.order_by('created_date').all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return CoreMemberSerializer
        if self.action in ['create', 'partial_update', 'update']:
            return CoreMemberSerializerCreate
        return CoreMemberSerializer

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

    def list(self, request):  # noqa: ignore=A003
        user = request.query_params.get('user')
        if user:
            try:
                members = CoreMember.objects.filter(user=user).order_by('created_date')
                page = self.paginate_queryset(members)
            except ValidationError:
                return Response(
                    {'detail': f'{user} is not a valid UUID'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except CoreMember.DoesNotExist:
                return Response(
                    {'detail': f'No CoreMember with User ID: {user} was found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer_class()
        serializer = serializer(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)


class ProjectMemberViewSet(CachedModelViewSet):
    filterset_fields = ['user']
    queryset = ProjectMember.objects.order_by('created_date').all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return ProjectMemberSerializer
        if self.action in ['create', 'partial_update', 'update']:
            return ProjectMemberSerializerCreate
        return ProjectMemberSerializer

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

    def list(self, request):  # noqa: ignore=AA03
        user = request.query_params.get('user')
        if user:
            try:
                members = ProjectMember.objects.filter(user=user)
                page = self.paginate_queryset(members)
            except ValidationError:
                return Response(
                    {'detail': f'{user} is not a valid UUID'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ProjectMember.DoesNotExist:
                return Response(
                    {'detail': f'No ProjectMember with User ID: {user} was found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer_class()
        serializer = serializer(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
