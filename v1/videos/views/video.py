from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from config.helpers.cache import CachedModelViewSet
from ..models.video import Video
from ..serializers.video import VideoSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class VideoViewSet(CachedModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request):  # noqa: ignore=A003
        if request.query_params.get('playlist'):
            playlist = request.query_params.get('playlist')
            try:
                videos = Video.objects.filter(playlist__uuid=playlist).order_by('created_date')
                videos = self.filter_queryset(videos)
                page = self.paginate_queryset(videos)
                serializer = self.get_serializer(page, context={'request': request}, many=True)
            except ValidationError:
                return Response({'detail': '{} is not a valid playlist uuid'.format(playlist)}, status=status.HTTP_400_BAD_REQUEST)
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
