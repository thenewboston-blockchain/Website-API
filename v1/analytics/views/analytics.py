from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models.community import Community
from ..models.economy import Economy
from ..models.network import Network
from ..serializers.community import CommunitySerializer
from ..serializers.economy import EconomySerializer
from ..serializers.network import NetworkSerializer


class CommunityViewset(ListModelMixin, GenericViewSet):
    queryset = Community.objects.all().order_by('week_ending')
    serializer_class = CommunitySerializer


class EconomyViewset(ListModelMixin, GenericViewSet):
    queryset = Economy.objects.all().order_by('week_ending')
    serializer_class = EconomySerializer


class NetworkViewset(ListModelMixin, GenericViewSet):
    queryset = Network.objects.all().order_by('week_ending')
    serializer_class = NetworkSerializer
