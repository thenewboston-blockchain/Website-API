from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from rest_framework import status, viewsets
from rest_framework.response import Response

from ..models.instructor import Instructor
from ..models.playlist import Playlist
from ..models.playlist_category import PlaylistCategory
from ..serializers.playlist import PlaylistSerializer, PlaylistSerializerCreate
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects \
        .select_related('instructor')\
        .prefetch_related(Prefetch('videos')) \
        .order_by('created_date') \
        .all()
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return PlaylistSerializer
        if self.action in ['create', 'partial_update', 'update']:
            return PlaylistSerializerCreate
        return PlaylistSerializer

    def list(self, request):  # noqa: ignore=A003
        if request.query_params.get('category') or request.query_params.get('instructor'):
            category = request.query_params.get('category')
            instructor = request.query_params.get('instructor')
            if category and not instructor:
                try:
                    category = PlaylistCategory.objects.get(name__iexact=category)
                    playlists = Playlist.objects.filter(categories__pk=category.pk).select_related('instructor').prefetch_related(Prefetch('videos')).order_by('created_date')
                except PlaylistCategory.DoesNotExist:
                    return Response({'detail': 'No playlist under category: {} was found'.format(category)}, status=status.HTTP_404_NOT_FOUND)
            elif instructor and not category:
                try:
                    playlists = Playlist.objects.filter(instructor__pk=instructor).order_by('created_date')
                except Instructor.DoesNotExist:
                    return Response({'detail': 'No playlist under instructor: {} was found'.format(instructor)}, status=status.HTTP_404_NOT_FOUND)
            elif category and instructor:
                try:
                    category = PlaylistCategory.objects.get(name__iexact=category)
                    playlists = Playlist.objects.filter(categories__pk=category.pk, instructor__pk=instructor).order_by('created_date')
                except PlaylistCategory.DoesNotExist:
                    return Response({'detail': 'No playlist under category: {} was found'.format(category)}, status=status.HTTP_404_NOT_FOUND)
                except ValidationError:
                    return Response({'detail': '{} is not a valid instructor uuid'.format(instructor)}, status=status.HTTP_400_BAD_REQUEST)
            playlists = self.filter_queryset(playlists)
            page = self.paginate_queryset(playlists)
            serializer = self.get_serializer_class()
            serializer = serializer(page, context={'request': request}, many=True)

        else:
            queryset = Playlist.objects \
                .select_related('instructor')\
                .prefetch_related(Prefetch('videos')) \
                .order_by('created_date') \
                .all()
            page = self.paginate_queryset(queryset)
            if not queryset:
                return Response({'detail': 'No playlists found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer_class()
            serializer = serializer(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
