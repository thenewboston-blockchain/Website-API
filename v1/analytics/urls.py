from rest_framework.routers import SimpleRouter

from .views.analytics import CommunityViewset, EconomyViewset, FacebookViewset, InstagramViewset,\
    LinkedInViewset, NetworkViewset, TwitterViewset


router = SimpleRouter(trailing_slash=False)
router.register('community_analytics', CommunityViewset)
router.register('economy_analytics', EconomyViewset)
router.register('network_analytics', NetworkViewset)
router.register('facebook_analytics', FacebookViewset)
router.register('instagram_analytics', InstagramViewset)
router.register('linkedin_analytics', LinkedInViewset)
router.register('twitter_analytics', TwitterViewset)
