from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.responsibility import Responsibility
from ..serializers.responsibility import ResponsibilitySerializer


class ResponsibilityViewSet(CachedModelViewSet):
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer
    permission_classes = [IsStaffOrReadOnly]
