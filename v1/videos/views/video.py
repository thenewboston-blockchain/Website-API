from django.core.exceptions import ValidationError
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
        if request.query_params.get('category') or request.query_params.get('playlist'):
            category = request.query_params.get('category')
            playlist = request.query_params.get('playlist')
            if category and not playlist:
                try:
                    category = Category.objects.get(name__iexact=category)
                    videos = Video.objects.filter(categories__pk=category.pk).order_by('created_date')
                except Category.DoesNotExist:
                    return Response({'detail': 'No video under category: {} was found'.format(category)}, status=status.HTTP_404_NOT_FOUND)
            elif playlist and not category:
                try:
                    videos = Video.objects.filter(playlist__uuid=playlist).order_by('created_date')
                except ValidationError:
                    return Response({'detail': '{} is not a valid playlist uuid'.format(playlist)}, status=status.HTTP_400_BAD_REQUEST)
            elif playlist and category:
                try:
                    category = Category.objects.get(name__iexact=category)
                    videos = Video.objects.filter(categories__pk=category.pk, playlist__uuid=playlist).order_by('created_date')
                except Category.DoesNotExist:
                    return Response({'detail': 'No video under category: {} was found'.format(category)}, status=status.HTTP_404_NOT_FOUND)
                except ValidationError:
                    return Response({'detail': '{} is not a valid playlist uuid'.format(playlist)}, status=status.HTTP_400_BAD_REQUEST)
            videos = self.filter_queryset(videos)
            page = self.paginate_queryset(videos)
            serializer = self.get_serializer(page, context={'request': request}, many=True)
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
