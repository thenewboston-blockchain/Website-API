# -*- coding: utf-8 -*-
from rest_framework import mixins, viewsets

from ..models import Skill
from ..serializers import SkillSerializer


class SkillViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = None
