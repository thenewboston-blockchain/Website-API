from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.response import Response

from config.helpers.cache import CachedModelViewSet
from ..models.instructor import Instructor
from ..models.playlist import Playlist
from ..models.playlist_category import PlaylistCategory
from ..serializers.playlist import PlaylistSerializer, PlaylistSerializerCreate
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class PlaylistViewSet(CachedModelViewSet):
    queryset = Playlist.objects \
        .select_related('instructor') \
        .prefetch_related(
            Prefetch('videos')
        )\
        .order_by('title')
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return PlaylistSerializer
        if self.action in ['create', 'partial_update', 'update']:
            return PlaylistSerializerCreate
        return PlaylistSerializer

    def list(self, request):  # noqa: ignore=A003
        if request.query_params.get('category') or request.query_params.get('instructor') or request.query_params.get('is_featured'):
            category = request.query_params.get('category')
            instructor = request.query_params.get('instructor')
            featured = request.query_params.get('is_featured')
            if featured and featured not in ['True', 'False', 'true', 'false']:
                return Response(
                    {'detail': 'Please provide a boolean value: True,False/true,false'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            arguments = {}
            for k, v in request.query_params.items():
                if v and k in ['instructor', 'is_featured']:
                    arguments[k] = v if k != 'is_featured' else featured.title()

            if category:
                try:
                    category = PlaylistCategory.objects.get(name__iexact=category)
                    playlists = Playlist.objects.filter(
                        categories__pk=category.pk,
                        **arguments
                    ).select_related(
                        'instructor'
                    ).prefetch_related(
                        Prefetch('videos')
                    ).order_by('created_date')
                except PlaylistCategory.DoesNotExist:
                    return Response(
                        {'detail': f'No playlist under category: {category} was found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                except ValidationError:
                    return Response(
                        {'detail': f'{instructor} is not a valid instructor uuid'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                try:
                    playlists = Playlist.objects.filter(**arguments).select_related(
                        'instructor'
                    ).prefetch_related(
                        Prefetch('videos')
                    ).order_by('created_date')
                except Instructor.DoesNotExist:
                    return Response(
                        {'detail': f'No playlist under instructor: {instructor} was found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                except ValidationError:
                    return Response(
                        {'detail': f'{instructor} is not a valid instructor uuid'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            playlists = self.filter_queryset(playlists)
            page = self.paginate_queryset(playlists)
            serializer = self.get_serializer_class()
            serializer = serializer(page, context={'request': request}, many=True)

        else:
            queryset = Playlist.objects \
                .select_related('instructor') \
                .prefetch_related(Prefetch('videos')) \
                .order_by('created_date')
            page = self.paginate_queryset(queryset)
            if not queryset:
                return Response({'detail': 'No playlists found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer_class()
            serializer = serializer(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
