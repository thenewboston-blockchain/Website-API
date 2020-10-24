# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views.team import TeamViewSet

router = SimpleRouter(trailing_slash=False)
router.register('teams', TeamViewSet)
