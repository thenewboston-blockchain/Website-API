# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views.user import UserViewSet
from .views.user_earnings import UserEarningsViewSet

router = SimpleRouter(trailing_slash=False)
router.register('user_earnings', UserEarningsViewSet)
router.register('users', UserViewSet)
