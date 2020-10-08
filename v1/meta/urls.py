# -*- coding: utf-8 -*-
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, ResponsibilityViewSet, SkillViewSet


router = SimpleRouter(trailing_slash=False)
router.register('category', CategoryViewSet)
router.register('responsibility', ResponsibilityViewSet)
router.register('skill', SkillViewSet)
