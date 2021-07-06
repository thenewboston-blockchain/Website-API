from rest_framework import status
from rest_framework.response import Response

from config.helpers.cache import CachedModelViewSet
from ..models.playlist_category import PlaylistCategory
from ..serializers.playlist_category import PlaylistCategorySerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class PlaylistCategoryViewSet(CachedModelViewSet):
    queryset = PlaylistCategory.objects \
        .order_by('name') \
        .all()
    serializer_class = PlaylistCategorySerializer
    permission_classes = [IsStaffOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['name'] = data['name'].lower() if isinstance(data['name'], str) else data['name']
        serializer = PlaylistCategorySerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Response(
            self.get_serializer(category).data,
            status=status.HTTP_201_CREATED
        )
