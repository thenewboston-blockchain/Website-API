from config.helpers.cache import CachedGenericViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.user_earnings import UserEarnings
from ..serializers.user_earnings import UserEarningsSerializer


class UserEarningsViewSet(CachedGenericViewSet):
    filterset_fields = ['repository__display_name', 'time_period']
    ordering = ['-total_amount']
    ordering_fields = ['total_amount']
    permission_classes = [IsStaffOrReadOnly]

    queryset = UserEarnings.objects.select_related('user')
    serializer_class = UserEarningsSerializer
