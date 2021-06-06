from rest_framework.routers import SimpleRouter

from .views.analytics import CommunityViewset, EconomyViewset


router = SimpleRouter(trailing_slash=False)
router.register('community_analytics', CommunityViewset)
router.register('economy_analytics', EconomyViewset)
