from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.roadmap import Roadmap
from ..serializers.roadmap import RoadmapSerializer


class RoadmapViewSet(CachedModelViewSet):
    queryset = Roadmap.objects.select_related('team').order_by('estimated_completion_date').all()
    serializer_class = RoadmapSerializer
    permission_classes = [IsStaffOrReadOnly]
