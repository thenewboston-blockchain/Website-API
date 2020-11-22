# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views.email import EmailViewSet

router = SimpleRouter(trailing_slash=False)
router.register('emails', EmailViewSet)
