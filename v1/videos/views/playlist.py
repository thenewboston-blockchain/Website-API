from rest_framework import mixins
from rest_framework import viewsets

from ..models.playlist import Playlist
from ..serializers.playlist import PlaylistSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
