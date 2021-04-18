from rest_framework.routers import SimpleRouter

from .views.milestone import MilestoneViewSet
from .views.project import ProjectViewSet

router = SimpleRouter(trailing_slash=False)
router.register('projects', ProjectViewSet)
router.register('milestones', MilestoneViewSet)
