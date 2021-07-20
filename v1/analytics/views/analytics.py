from django.db.models import Prefetch

from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.analytics import Analytics, AnalyticsCategory, AnalyticsData
from ..serializers.analytics import AnalyticsCategorySerializer, AnalyticsCategorySerializerCreate,\
    AnalyticsDataSerializer, AnalyticsSerializer


class AnalyticsCategoryViewSet(CachedModelViewSet):
    queryset = AnalyticsCategory.objects \
        .prefetch_related(Prefetch('analytics'),) \
        .all()

    serializer_class = AnalyticsCategorySerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrive':
            return AnalyticsCategorySerializer
        if self.action in ['create', 'partial_update', 'update']:
            return AnalyticsCategorySerializerCreate
        return AnalyticsCategorySerializer


class AnalyticsViewSet(CachedModelViewSet):
    queryset = Analytics.objects \
        .prefetch_related(Prefetch('data'),) \
        .all()

    serializer_class = AnalyticsSerializer
    permission_classes = [IsStaffOrReadOnly]


class AnalyticsDataViewSet(CachedModelViewSet):
    queryset = AnalyticsData.objects.select_related('analytics').order_by('date').all()

    serializer_class = AnalyticsDataSerializer
    permission_classes = [IsStaffOrReadOnly]
