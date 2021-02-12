from rest_framework.viewsets import ModelViewSet

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.slack_channel import SlackChannel
from ..serializers.team import SlackChannelSerializer


class SlackChannelViewSet(ModelViewSet):
    queryset = SlackChannel.objects.all()
    serializer_class = SlackChannelSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
