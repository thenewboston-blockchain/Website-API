# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views.repository import RepositoryViewSet

router = SimpleRouter(trailing_slash=False)
router.register('repositories', RepositoryViewSet)
