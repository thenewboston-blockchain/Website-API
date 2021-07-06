from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.repository import Repository
from ..serializers.repository import RepositorySerializer


class RepositoryViewSet(CachedModelViewSet):
    queryset = Repository.objects.order_by('created_date').all()
    serializer_class = RepositorySerializer
    permission_classes = [IsStaffOrReadOnly]
