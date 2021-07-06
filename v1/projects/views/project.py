from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.project import Project
from ..serializers.project import ProjectSerializer


class ProjectViewSet(CachedModelViewSet):
    queryset = Project.objects.all().select_related('project_lead__user').order_by('title')
    serializer_class = ProjectSerializer
    permission_classes = [IsStaffOrReadOnly]
