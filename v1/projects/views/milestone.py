from rest_framework.viewsets import ModelViewSet

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.milestone import Milestone
from ..serializers.milestone import MilestoneSerializer


class MilestoneViewSet(ModelViewSet):
    queryset = Milestone.objects.order_by('created_date').all()
    serializer_class = MilestoneSerializer
    permission_classes = [IsStaffOrReadOnly]
