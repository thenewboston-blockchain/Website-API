from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ModelViewSet

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly, IsSuperUserOrReadOnly
from ..models.feedback import Feedback
from ..serializers.feedback import FeedbackSerializer


class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsStaffOrReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            permission_classes = [IsSuperUserOrReadOnly]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
