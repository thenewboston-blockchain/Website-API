from django.db.models import Prefetch

from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.app import App, AppImage
from ..serializers.app import AppImageSerializer, AppSerializer, AppSerializerCreate


class AppViewSet(CachedModelViewSet):
    queryset = App.objects \
        .prefetch_related(Prefetch('images'),) \
        .all()
    serializer_class = AppSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return AppSerializer
        if self.action in ['create', 'partial_update', 'update']:
            return AppSerializerCreate
        return AppSerializer


class AppImageViewSet(CachedModelViewSet):
    queryset = AppImage.objects.all()
    serializer_class = AppImageSerializer
    permission_classes = [IsStaffOrReadOnly]
