from rest_framework import viewsets

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.responsibility import Responsibility
from ..serializers.responsibility import ResponsibilitySerializer


class ResponsibilityViewSet(viewsets.ModelViewSet):
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
