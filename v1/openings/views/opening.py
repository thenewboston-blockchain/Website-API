# -*- coding: utf-8 -*-
from django.db.models import Prefetch
from rest_framework import viewsets

from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from v1.users.models.user import User
from ..models import Opening
from ..serializers import OpeningSerializer


class OpeningViewSet(viewsets.ModelViewSet):
    queryset = Opening.objects.prefetch_related(
        Prefetch(
            'team__team_members',
            queryset=User.objects.filter(teammember__is_lead=True),
        ),
        'responsibilities',
        'skills'
    ).order_by(
        'created_date'
    ).all()

    serializer_class = OpeningSerializer
    pagination_class = None
    permission_classes = [IsStaffOrReadOnly]
