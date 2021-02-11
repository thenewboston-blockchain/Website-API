from rest_framework import viewsets

from ..models.playlist import Playlist
from ..serializers.playlist import PlaylistSerializer
# from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects \
        .prefetch_related('videos') \
        .order_by('created_date') \
        .all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsStaffOrReadOnly]
