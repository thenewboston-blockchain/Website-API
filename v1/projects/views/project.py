from rest_framework import status
from rest_framework.response import Response

from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.project import Project
from ..serializers.project import ProjectSerializer


class ProjectViewSet(CachedModelViewSet):
    queryset = Project.objects.all().select_related('project_lead__user').order_by('title')
    serializer_class = ProjectSerializer
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request):  # noqa: ignore=A003
        is_featured = request.query_params.get('is_featured')
        if is_featured:
            if is_featured not in ['True', 'False', 'true', 'false']:
                return Response(
                    {'detail': 'Please provide a boolean value: True,False/true,false'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            projects = Project.objects.filter(is_featured=is_featured.title()).select_related('project_lead__user').order_by('title')
            projects = self.filter_queryset(projects)
            page = self.paginate_queryset(projects)
            serializer = self.serializer_class(page, context={'request': request}, many=True)
        else:
            page = self.paginate_queryset(self.queryset)
            serializer = self.serializer_class(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
