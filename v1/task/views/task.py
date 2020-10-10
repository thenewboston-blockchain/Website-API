# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models import Task
from ..serializers import TaskSerializer
from ...third_party.rest_framework.permissions import IsStaffOrReadOnly


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects \
        .select_related('contributor') \
        .order_by('created_date') \
        .all()
    serializer_class = TaskSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
