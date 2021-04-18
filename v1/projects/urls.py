from rest_framework.routers import SimpleRouter

from .views.project import ProjectViewSet

router = SimpleRouter(trailing_slash=False)
router.register('projects', ProjectViewSet)
