from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.category import Category
from ..models.playlist import Playlist
from ..serializers.playlist import PlaylistSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects \
        .prefetch_related('videos') \
        .order_by('created_date') \
        .all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request):  # noqa: ignore=A003
        if request.query_params.get('category'):
            category = request.query_params.get('category')
            try:
                category = Category.objects.get(name=category)
                playlists = Playlist.objects.filter(categories__pk=category.pk).prefetch_related('videos').order_by('created_date')
                page = self.paginate_queryset(playlists)
                serializer = self.get_serializer(page, context={'request': request}, many=True)
            except Category.DoesNotExist:
                return Response({'detail': 'No playlist under category "{}" was found'.format(category)}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Playlist.objects\
                .prefetch_related('videos')\
                .order_by('created_date')\
                .all()
            page = self.paginate_queryset(queryset)
            if not queryset:
                return Response({'detail': 'No playlists found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
