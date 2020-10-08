# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import Skill
from ..serializers import SkillSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
