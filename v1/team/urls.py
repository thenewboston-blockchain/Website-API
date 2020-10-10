# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views import ContributorViewSet, TeamViewSet


router = SimpleRouter(trailing_slash=False)
router.register('contributor', ContributorViewSet)
router.register('team', TeamViewSet)
