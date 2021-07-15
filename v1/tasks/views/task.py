from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.task import Task
from ..serializers.task import TaskSerializer


class TaskViewSet(CachedModelViewSet):
    queryset = Task.objects \
        .select_related('user') \
        .order_by('created_date') \
        .all()
    serializer_class = TaskSerializer
    permission_classes = [IsStaffOrReadOnly]
