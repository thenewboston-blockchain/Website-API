from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models.community import Community
from ..serializers.community import CommunitySerializer


class CommunityViewset(ListModelMixin, GenericViewSet):
    queryset = Community.objects.all().order_by('week_ending')
    serializer_class = CommunitySerializer
