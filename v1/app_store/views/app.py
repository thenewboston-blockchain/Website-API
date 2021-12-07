from django.db.models import Prefetch
from rest_framework import status
from rest_framework.response import Response

from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.app import App, AppImage, Category
from ..serializers.app import AppImageSerializer, AppSerializer, AppSerializerCreate, CategorySerializer


class AppViewSet(CachedModelViewSet):
    queryset = App.objects \
        .prefetch_related(Prefetch('images'),) \
        .all()
    serializer_class = AppSerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
        except App.MultipleObjectsReturned:
            instances = App.objects.filter(slug=kwargs['slug'])
            if instances:
                serializer = self.get_serializer(instances[0])
            else:
                return Response(
                    {'detail': 'Not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.data)

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


class CategoryViewSet(CachedModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]
