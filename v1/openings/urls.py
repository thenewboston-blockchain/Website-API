# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views import OpeningViewSet, ResponsibilityViewSet, SkillViewSet

router = SimpleRouter(trailing_slash=False)
router.register('openings', OpeningViewSet)
router.register('responsibilities', ResponsibilityViewSet)
router.register('skills', SkillViewSet)
