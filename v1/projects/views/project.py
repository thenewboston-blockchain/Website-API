from rest_framework.viewsets import ModelViewSet

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.project import Project
from ..serializers.project import ProjectSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.order_by('created_date').all()
    serializer_class = ProjectSerializer
    permission_classes = [IsStaffOrReadOnly]
