from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.analytics import Analytics, AnalyticsCategory, AnalyticsData
from ..serializers.analytics import AnalyticsCategorySerializer,\
    AnalyticsDataSerializer, AnalyticsSerializer


class AnalyticsCategoryViewSet(CachedModelViewSet):
    queryset = AnalyticsCategory.objects \
        .prefetch_related(Prefetch('analytics'),) \
        .all()

    serializer_class = AnalyticsCategorySerializer
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request):  # noqa: ignore=A003
        if request.query_params.get('key'):
            key = request.query_params.get('key')
            try:
                categories = AnalyticsCategory.objects.filter(
                    key__iexact=key).prefetch_related(Prefetch('analytics'),).order_by('created_date')
            except AnalyticsCategory.DoesNotExist:
                return Response(
                    {'detail': f'No AnalyticsCategory under key: {key} was found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            categories = self.filter_queryset(categories)
            page = self.paginate_queryset(categories)
            serializer = self.serializer_class(page, context={'request': request}, many=True)
        else:
            page = self.paginate_queryset(self.queryset)
            serializer = self.serializer_class(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)


class AnalyticsViewSet(CachedModelViewSet):
    queryset = Analytics.objects \
        .prefetch_related(Prefetch('data'),) \
        .all()

    serializer_class = AnalyticsSerializer
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request):  # noqa: ignore=A003
        if request.query_params.get('category'):
            key = request.query_params.get('category')
            try:
                category = AnalyticsCategory.objects.get(
                    key__iexact=key)
                analytics = category.analytics.all()
            except AnalyticsCategory.DoesNotExist:
                return Response(
                    {'detail': f'No Analytics under category: {key} found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            analytics = self.filter_queryset(analytics)
            page = self.paginate_queryset(analytics)
            serializer = self.serializer_class(page, context={'request': request}, many=True)
        else:
            page = self.paginate_queryset(self.queryset)
            serializer = self.serializer_class(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)


class AnalyticsDataViewSet(ModelViewSet):
    queryset = AnalyticsData.objects.select_related('analytics').order_by('date').all()

    serializer_class = AnalyticsDataSerializer
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request):  # noqa: ignore=A003
        analytics_id = request.query_params.get('analytics')
        since = request.query_params.get('from', '1970-01-01')
        until = request.query_params.get('to', '3030-12-30')
        if analytics_id or since or until:
            try:
                if analytics_id:
                    analytics_data = AnalyticsData.objects.filter(analytics__pk=analytics_id, date__gte=since, date__lte=until).select_related('analytics').order_by('date')
                else:
                    analytics_data = AnalyticsData.objects.filter(date__gte=since, date__lte=until).select_related('analytics').order_by('date')
            except AnalyticsData.DoesNotExist:
                return Response(
                    {'detail': 'No AnalyticsData with given parameters was found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            except ValidationError as e:
                if 'must be in YYYY-MM-DD HH:MM' in str(e):
                    return Response(
                        {'detail': 'Invalid date format, date must be in "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]" or "YYYY-MM-DD" '},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {'detail': f'{analytics_id} is not a valid Analytics uuid'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            analytics_data = self.filter_queryset(analytics_data)
            page = self.paginate_queryset(analytics_data)
            serializer = self.get_serializer_class()
            serializer = serializer(page, context={'request': request}, many=True)
        else:
            page = self.paginate_queryset(self.queryset)
            serializer = self.get_serializer_class()
            serializer = serializer(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
