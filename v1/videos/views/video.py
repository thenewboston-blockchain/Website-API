from rest_framework import viewsets

from ..models.video import Video
from ..serializers.video import VideoSerializer
# from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = None
    # permission_classes = [IsStaffOrReadOnly]
