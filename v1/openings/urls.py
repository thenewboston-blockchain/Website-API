from rest_framework.routers import SimpleRouter

from .views.opening import OpeningViewSet
from .views.responsibility import ResponsibilityViewSet
from .views.skill import SkillViewSet

router = SimpleRouter(trailing_slash=False)
router.register('openings', OpeningViewSet)
router.register('responsibilities', ResponsibilityViewSet)
router.register('skills', SkillViewSet)
