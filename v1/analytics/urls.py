from rest_framework.routers import SimpleRouter

from .views.analytics import CommunityViewset, EconomyViewset, NetworkViewset


router = SimpleRouter(trailing_slash=False)
router.register('community_analytics', CommunityViewset)
router.register('economy_analytics', EconomyViewset)
router.register('network_analytics', NetworkViewset)
