# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views import OpeningViewSet


router = SimpleRouter(trailing_slash=False)
router.register('opening', OpeningViewSet)
