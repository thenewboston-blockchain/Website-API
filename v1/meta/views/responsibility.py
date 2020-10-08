# -*- coding: utf-8 -*-
from rest_framework import mixins, viewsets

from ..models import Responsibility
from ..serializers import ResponsibilitySerializer


class ResponsibilityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer
    pagination_class = None
