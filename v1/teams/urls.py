# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views.team import TeamViewSet
from .views.team_member import TeamMemberViewSet

router = SimpleRouter(trailing_slash=False)
router.register('team_members', TeamMemberViewSet)
router.register('teams', TeamViewSet)
