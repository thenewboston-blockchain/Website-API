# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views import TeamViewSet

router = SimpleRouter(trailing_slash=False)
router.register('teams', TeamViewSet)
