from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models.community import Community
from ..models.economy import Economy
from ..serializers.community import CommunitySerializer
from ..serializers.economy import EconomySerializer


class CommunityViewset(ListModelMixin, GenericViewSet):
    queryset = Community.objects.all().order_by('week_ending')
    serializer_class = CommunitySerializer


class EconomyViewset(ListModelMixin, GenericViewSet):
    queryset = Economy.objects.all().order_by('week_ending')
    serializer_class = EconomySerializer
