from rest_framework.routers import SimpleRouter

from .views.analytics import AnalyticsCategoryViewSet, AnalyticsDataViewSet, AnalyticsViewSet


router = SimpleRouter(trailing_slash=False)
router.register('analytics_categories', AnalyticsCategoryViewSet)
router.register('analytics', AnalyticsViewSet)
router.register('analytics_data', AnalyticsDataViewSet)
