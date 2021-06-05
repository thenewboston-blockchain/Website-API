from rest_framework.routers import SimpleRouter

from .views.community import CommunityViewset

router = SimpleRouter(trailing_slash=False)
router.register('community_analytics', CommunityViewset)
