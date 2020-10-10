# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views import TaskViewSet


router = SimpleRouter(trailing_slash=False)
router.register('task', TaskViewSet)
