from rest_framework.routers import SimpleRouter

from .views.roadmap import RoadmapViewSet

router = SimpleRouter(trailing_slash=False)
router.register('roadmap', RoadmapViewSet)
