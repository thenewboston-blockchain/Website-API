# -*- coding: utf-8 -*-
from rest_framework import viewsets

from ..models.email import Email
from ..serializers.email import EmailSerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects \
        .order_by('created_at') \
        .all()
    serializer_class = EmailSerializer
    pagination_class = None
