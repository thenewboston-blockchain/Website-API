from rest_framework import mixins

from config.helpers.cache import CachedGenericViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.trusted_bank import TrustedBank
from ..serializers.trusted_bank import TrustedBankSerializer


class TrustedBankViewSet(mixins.RetrieveModelMixin,
                         CachedGenericViewSet):
    queryset = TrustedBank.objects.all()
    serializer_class = TrustedBankSerializer
    permission_classes = [IsStaffOrReadOnly]
