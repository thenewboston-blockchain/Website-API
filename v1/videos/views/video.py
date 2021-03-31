from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models.category import Category
from ..models.video import Video
from ..serializers.video import VideoSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request):  # noqa: ignore=A003
        if request.query_params.get('category'):
            category = request.query_params.get('category')
            try:
                category = Category.objects.get(name=category)
                playlists = Video.objects.filter(categories__pk=category.pk).order_by('created_date')
                playlists = self.filter_queryset(playlists)
                page = self.paginate_queryset(playlists)
                serializer = self.get_serializer(page, context={'request': request}, many=True)
            except Category.DoesNotExist:
                return Response({'detail': 'No video under category "{}" was found'.format(category)}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Video.objects\
                .order_by('created_date')\
                .all()
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if not queryset:
                return Response({'detail': 'No videos found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
