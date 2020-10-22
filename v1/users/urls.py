# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

router = SimpleRouter(trailing_slash=False)
router.register('users', UserViewSet)
